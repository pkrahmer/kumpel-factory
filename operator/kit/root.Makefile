# Forwards every target to the factory's makefile, so that `make check` works at the root.
# For a repository without a root Makefile of its own; copied from kumpel-factory's kit as `Makefile`.
.DEFAULT_GOAL := check
Makefile: ;
.PHONY: factory-forward
factory-forward: ;
%: factory-forward
	@$(MAKE) --no-print-directory -f factory/Makefile $@
