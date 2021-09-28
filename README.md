# Knowledge tracing data fiddler

A python project that allows easy management of knowledge tracing data

- Easy conversion between commonly used data format
- Data cleaning
  - Convert non-binary correctnesses into binary correctness
  - Remove (csv) rows where critical values are missing
- Group non-grouped data by students to obtain attempt sequences per student
- Filter data
  - By maximum attempt count (by splitting or cutting)
  - By minimum attempt count
- Split into train and test set
- Split into kfold train and test sets
- Print data statistics in different formats

## Attempts-skills-corrects (asc) format

 Contains student attempt sequences in row triples that contain:

 1. Number of attempts
 2. Skill ids of attempts
 3. Attempt correctnesses

Example contents for two students:

 ```
3
1,2,3
0,0,1
2
1,1
0,1
```

## Requirements

Python >3.6

```sh
conda install scikit-learn pandas
```

or (use pip3 if pip points to python 2)

```sh
pip install scikit-learn pandas
```

## Usage

From csv to asc format using default column names.

```sh
python converter.py my.csv my.asc --out-format asc
```

From  to yudelson-bkt (hmm-scalable) format with
specified column names

```sh
python converter.py my.csv my.tsv --out-format yudelson-bkt --user-col student-id --exercise-col problem-id --skill-col problem-id --correct-col is-correct
```

Show all options

```sh
python converter.py -h
```

## Running tests

```sh
python -m unittest discover -s tests
```
