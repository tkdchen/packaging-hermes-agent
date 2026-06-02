build_package() {
    local -r name=${1:?Missing package name}
    local -r pkg_dir="./packages/${name}/"
    local -r spec="${pkg_dir}/python-${name}.spec"
    local -r result_dir="./results/${name}"
    [[ -e "$result_dir" ]] || mkdir -p "$result_dir"
    make -f .copr/Makefile local=true outdir="$pkg_dir" spec="$spec"
    mapfile -t srpm_files < <(find "./packages/${name}" -name "python-${name}-*.fc??.src.rpm")
    if [[ ${#srpm_files[@]} -eq 1 ]]; then
	mock --rebuild --root fedora-rawhide-x86_64 --resultdir "$result_dir" "${srpm_files[0]}"
    else
	printf "Cannot start mock build. Check SRPM under ${pkg_dir}\n" >&2
	return 1
    fi
}

build_package "$@"
