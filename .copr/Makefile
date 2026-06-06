
ifeq ($(local),true)
sources_dir = ~/rpmbuild/SOURCES/
else
sources_dir = /builddir/build/SOURCES/
endif

.PHONY: source
source:
	if [ -z "$(local)" ]; then exit 0; fi; \
	source_url=$$(rpmspec --parse $(spec) | grep -E "^Source: +" | sed -E 's/^Source: +//') && \
	printf "⬇️ Download source from %s\n" "$$source_url" >&2; \
	cd $(sources_dir) && curl -LO "$${source_url}"; \
	printf "Downloaded file: %s%s\n" "$(sources_dir)" "$$(basename $$source_url)"

.PHONY: srpm
srpm: source
	grep -E "^Patch: " $(spec) | while read -r prefix filename; do \
		echo "Patch: $${filename}"; \
		cp "$$(dirname $(spec))/$${filename}" $(sources_dir); \
	done; \
	srpm_file=$$(rpmbuild -bs $(spec) | grep "^Wrote:" | cut -d' ' -f2) ; \
	printf "📦 Generated SRPM: %s\n" "$$srpm_file" >&2; \
	cp "$${srpm_file}" "$(outdir)"; \
	printf "SRPM %s is copied to %s\n" "$$srpm_file" "$(outdir)" >&2
