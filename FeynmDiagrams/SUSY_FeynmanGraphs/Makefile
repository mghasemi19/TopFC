# find all sources
SRC:=$(shell ls *.tex|grep -v allDiagrams.tex)

# make list of plots
PDF=$(SRC:%.tex=%.pdf)

# by default make all plots
plots: $(PDF)

# use all to make the summary docs
all: allDiagrams.pdf allDiagrams.twiki
	ls *.tex | grep -v allDiagrams.tex | grep -v ATLAS-SUSY.tex | sort > tmpListInDir.txt; awk -F "{|}" '/graph{/{print $$2".tex"}' allDiagrams.tex | sort > tmpListInAll.txt; echo "\n THESE DIAGRAMS ARE NOT IN allDiagrams.tex\n"; diff tmpListInDir.txt tmpListInAll.txt; rm tmpListInDir.txt tmpListInAll.txt

# special rule for the summary document
allDiagrams.pdf: allDiagrams.tex $(PDF)
	pdflatex allDiagrams.tex; pdflatex allDiagrams.tex; rm -f allDiagrams.aux allDiagrams.log allDiagrams.toc allDiagrams.out

# rule to make the pdf, eps and png files
%.pdf: %.tex
	pdflatex $<; test $(@:%.pdf=%TMP) && mpost $(@:%.pdf=%TMP); pdflatex $<; pdfcrop --margins 3 $@ $@.tmp; mv $@.tmp $@; pdf2ps $@ $(@:%.pdf=%.eps); rm -f $(@:%.pdf=%TMP)* $(@:%.pdf=%.aux) $(@:%.pdf=%.log); convert -scale 800x600 -density 600 -quality 100 $@ $(@:%.pdf=%.png)

allDiagrams.twiki: allDiagrams.tex
	sed -n 's/.*\\graph{\(.*\)}.*/%GRAPH{"\1"}%/p;s/.*\\section{\(.*\)}.*/---+ \1/p' $< > $@

# clean unnecessary files
clean:
	rm -f *.aux *.log *.toc

