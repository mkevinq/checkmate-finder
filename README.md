[![Work in Repl.it](https://classroom.github.com/assets/work-in-replit-14baed9a392b3a25080506f3b7b6d57f295ec2978f6f33ec97e36a161684cbe9.svg)](https://classroom.github.com/online_ide?assignment_repo_id=317310&assignment_repo_type=GroupAssignmentRepo)

# CISC/CMPE 204 Modelling Project

Welcome to the major project for group 110 in CISC/CMPE 204 (Fall 2020)!

Our project is designed to find if a given board (of variable size) is or can be made into checkmate (using given pieces). Essentially, the constraints describe the movements of chess pieces, and the model will be satisfiable if checkmate is reach. If you want to give the system a starting board configuration, and additional pieces then it will attempt to place those pieces so that checkmate is reached (and will count how many possible solutions there are). If checkmate cannot be reached, then the model is not satisfiable.

## Structure

* `documents`: Contains folders for both of our draft and final submissions. README.md files are included in both.
* `run.py`: General wrapper script that contains all relevant code. The model, constraints, propositions, and all other code is contained here.
* `test.py`: Tests to confirm that this submission has everything required. This essentially just means it will check for the right files and sufficient theory size.

## Contact

If there are any questions regarding the project, implementation, documentation, or otherwise, feel free to contact us! Here are our emails:

* Callum Kipin - 18cgwk@queensu.ca
* Evan Kilburn - 18ewk@queensu.ca
* Kevin Quijalvo - 18mkq@queensu.ca
* Steven Wen - 18yw85@queensu.ca
