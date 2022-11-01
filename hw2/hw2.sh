#!/bin/sh

usage() {
    echo "hw2.sh -i INPUT -o OUTPUT [-c csv|tsv] [-j]"
    echo
    echo "Available Options:"
    echo
    echo "-i: Input file to be decoded"
    echo "-o: Output directory"
    echo "-c csv|tsv: Output files.[ct]sv"
    echo "-j: Output info.json"
}

check_input_extension() {
    local extension="${input_file##*.}"
    if [ "${extension}" != "hw2" ] ; then
        echo "Error: input file should have an extension '.hw2'" > /dev/stderr
        usage > /dev/stderr
        exit 1
    fi
}

make_dirs_for_file() {
    local folders="${1%/*}"
    mkdir -p ${folders}
}

output_info_json() {
    local info_json_path="${output_dir%/}/info.json"

    make_dirs_for_file "${info_json_path}"

    local info_json=$(jq --null-input \
        --arg name "${file_name}" \
        --arg author "${file_author}" \
        --arg date $(date -d @${file_date} -Iseconds) \
        '{name:$name, author:$author, date:$date}')
    
    echo "${info_json}" > "${info_json_path}"
}

output_listed_file() {
    # extract attributes
    file_name=$(echo "${1}" | jq -r '.name')
    local file_content=$(echo "${1}" | jq -r '.data' | base64 -d)

    # write content to specified location, expose the output path (for checksum)
    file_path="${output_dir}/${file_name}"
    make_dirs_for_file "${file_path}"
    echo "${file_content}" > "${file_path}"

    # expose file size (needed in files.[ct]sv)
    file_size=$(ls -l ${file_path} | awk '{print $5}')
}

load_checksum() {
    stored_md5=$(echo "${file_detail}" | jq -r '.hash.md5')
    stored_sha1=$(echo "${file_detail}" | jq -r '.hash."sha-1"')
}

ctsv_write_header() {
    local output_file="${output_dir}/files.${output_format}"
    make_dirs_for_file "${output_file}"
    printf "filename${separator}size${separator}md5${separator}sha1\n" > "${output_file}"
}

ctsv_write_record() {
    local output_file="${output_dir}/files.${output_format}"
    printf "${file_name}${separator}${file_size}${separator}${file_md5sum}${separator}${file_sha1sum}\n" >> "${output_file}"
}

input_file=""
output_dir=""
output_format=""
separator=""
output_json=0

# handle options
while getopts ":i:o:c:j" op; do
    case $op in
        i)
            input_file="${OPTARG}"
            check_input_extension
            ;;
        o)
            output_dir="${OPTARG}"
            ;;
        c)
            if [ "${OPTARG}" = "csv" ]; then
                output_format="csv"
                separator=","
            elif [ "${OPTARG}" = "tsv" ]; then
                output_format="tsv"
                separator="\t"
            else
                echo "Invalid format: '${OPTARG}'"
                usage > /dev/stderr
                exit 1
            fi
            ;;
        j)
            output_json=1
            ;;
        ?)
            usage > /dev/stderr
            exit 1
    esac
done

# check if input file exists, if not, terminate the program.
if ! ([ "${input_file}" ] && [ -f "${input_file}" ]); then
    echo "Error: input file '${input_file}' not found" > /dev/stderr
    exit 1
fi

# extract attributes
file_name=$(jq -r '.name' "${input_file}")
file_author=$(jq -r '.author' "${input_file}")
file_date=$(jq -r '.date' "${input_file}")
file_list_length=$(jq '.files | length' "${input_file}")

if [ "${output_json}" = 1 ]; then
    output_info_json
fi

if [ "${output_format}" ]; then
    ctsv_write_header
fi

invalid=0

for i in $(seq 0 $((${file_list_length} - 1))); do
    file_detail=$(jq ".files | .[${i}]" "${input_file}")
    output_listed_file "${file_detail}"
    file_md5sum=$(md5sum ${file_path} | cut -d ' ' -f1)
    file_sha1sum=$(sha1sum ${file_path} | cut -d ' ' -f1)

    stored_md5=$(echo "${file_detail}" | jq -r '.hash.md5')
    stored_sha1=$(echo "${file_detail}" | jq -r '.hash."sha-1"')

    if [ "${stored_md5}" != "${file_md5sum}" ] || [ "${stored_sha1}" != "${file_sha1sum}" ]; then
        invalid=$(( ${invalid} + 1 ))
    fi

    if [ "${output_format}" ]; then
        ctsv_write_record
    fi
done

exit ${invalid}
