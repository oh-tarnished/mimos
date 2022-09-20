#!/bin/sh

usage() { echo "Usage: $0 -f <path to blend file> -a <action name>" 1>&2; exit 1; }


while getopts ":f:a:" o; do
    case "${o}" in
        f)
            BLEND_FILE=${OPTARG}
            ;;
        a)
            ACTION=${OPTARG}
            ;;
        *)
            usage
    esac
done
shift $((OPTIND-1))

if [ -z "${BLEND_FILE}" ] || [ -z "${ACTION}" ]; then
    usage
fi

# starting blender
blender -y $BLEND_FILE -P animationoperator.py -- $ACTION
