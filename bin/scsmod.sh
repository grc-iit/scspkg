#!/bin/bash

scsmod() {
    local action="$1"
    shift  # Remove the action from arguments

    case "$action" in
        "load")
            local cmd_output
            cmd_output=$(scspkg module load $@)
            local exit_status=$?
            if [ $exit_status -ne 0 ]; then
                scspkg module load $@
                return $exit_status
            fi
            eval "$cmd_output"
            ;;
        "unload")
            local cmd_output
            cmd_output=$(scspkg module unload $@)
            local exit_status=$?
            if [ $exit_status -ne 0 ]; then
                scspkg module unload
                return $exit_status
            fi
            eval "$cmd_output"
            ;;
        *)
            echo "Usage: scsmod load <module_name> [<module_name> ...]"
            return 1
            ;;
    esac
}