.PHONY: pdf clean notebooks results validation

# Compile the thesis
pdf:
	latexmk -pdf main.tex

# Remove LaTeX build artifacts
clean:
	latexmk -C main.tex
	rm -f main.bbl

# Regenerate ALL notebooks from their builder scripts, then execute them
notebooks:
	cd Code && \
	python3 build_notebooks.py && \
	python3 build_nb_validation.py && \
	python3 build_nb_results.py && \
	jupyter nbconvert --to notebook --execute nb_model_A.ipynb   --output nb_model_A.ipynb   --ExecutePreprocessor.timeout=300 && \
	jupyter nbconvert --to notebook --execute nb_model_B.ipynb   --output nb_model_B.ipynb   --ExecutePreprocessor.timeout=300 && \
	jupyter nbconvert --to notebook --execute nb_model_B2.ipynb  --output nb_model_B2.ipynb  --ExecutePreprocessor.timeout=300 && \
	jupyter nbconvert --to notebook --execute nb_model_C2.ipynb  --output nb_model_C2.ipynb  --ExecutePreprocessor.timeout=300 && \
	jupyter nbconvert --to notebook --execute nb_model_X.ipynb   --output nb_model_X.ipynb   --ExecutePreprocessor.timeout=300 && \
	jupyter nbconvert --to notebook --execute nb_validation.ipynb --output nb_validation.ipynb --ExecutePreprocessor.timeout=300 && \
	jupyter nbconvert --to notebook --execute nb_results.ipynb   --output nb_results.ipynb   --ExecutePreprocessor.timeout=300

# Regenerate and execute only the results notebook
results:
	cd Code && python3 build_nb_results.py && \
	jupyter nbconvert --to notebook --execute nb_results.ipynb --output nb_results.ipynb --ExecutePreprocessor.timeout=300

# Regenerate and execute only the validation notebook
validation:
	cd Code && python3 build_nb_validation.py && \
	jupyter nbconvert --to notebook --execute nb_validation.ipynb --output nb_validation.ipynb --ExecutePreprocessor.timeout=300
