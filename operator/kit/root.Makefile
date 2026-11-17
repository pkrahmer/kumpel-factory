# Forwards every target to the factory's makefile, so that `make check` works at the root.
# For a repository without a root Makefile of its own; copied from kumpel-factory's kit as `Makefile`.
.DEFAULT_GOAL := check
Makefile: ;
%:
	@$(MAKE) --no-print-directory -f factory/Makefile $@
