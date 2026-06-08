
ifeq ($(local),true)
sources_dir = ~/rpmbuild/SOURCES/
else
sources_dir = /builddir/build/SOURCES/
endif

.PHONY: source
source:
	if [ -z "$(local)" ]; then exit 0; fi; \
	rpmspec --parse $(spec) | grep -E "^Source: +" | while read -r prefix source_file; \
	do \
		if [[ $${source_file} =~ ^https://.+ ]]; then \
			printf "⬇️ Download source from %s\n" "$$source_file" >&2; \
			curl -C - -L -o $(sources_dir)$$(basename "$$source_file") "$${source_file}"; \
			printf "Downloaded file: %s%s\n" "$(sources_dir)" "$$(basename $$source_file)"; \
		else \
			local_source_file="$$(dirname "$(spec)")/$${source_file}"; \
			cp "$$local_source_file" $(sources_dir); \
			printf "Copied local source file %s to %s\n" "$$local_source_file" "$(sources_dir)"; \
		fi; \
	done

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
