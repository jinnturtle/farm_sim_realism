SRC_DIR=src
#TEX_COMPILER=--latex=pdflatex --pdf
#TEX_COMPILER=--lualatex
TEX_COMPILER=--xelatex --pdf
OUT_DIR=out
TEX_OUT=$(OUT_DIR)/jinns_realism.pdf 

all: $(OUT_DIR) $(TEX_OUT)

$(OUT_DIR)/%.pdf: $(SRC_DIR)/%/main.tex makefile
	latexmk -cd $(TEX_COMPILER) --output-directory=$(abspath $(dir $@)) --jobname=$(basename $(notdir $@)) $<
	# clean up the auxiliary files
	latexmk -c -cd $(TEX_COMPILER) --output-directory=$(abspath $(dir $@)) --jobname=$(basename $(notdir $@)) $<

$(OUT_DIR):
	mkdir -p $@

.PHONY=clean
clean: 
	@rm -rvf $(OUT_DIR)
