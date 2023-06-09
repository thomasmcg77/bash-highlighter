# bash-highlighter

### Language Being Parsed

The language I am parsing is bash. While I was not able to implement every feature of bash, it is able to parse the most used commands. The program will output the text provided with colors using ANSI escape codes. Each type (command, string, operator, etc.) will have a different color and acts as a sort of simulation of a syntax highlighter.

### Note
One thing to note is that newline characters don't register in the input. If you want to test multi-line scripts, you can replace the input() function assigned to the 'script' variable with a string. Now when you run the program it will automatically output to the terminal instead of prompting you for a script in the terminal. Another thing to note is that loops don't currently work in the parser. They can be parsed when my grammar is used in the Lark online IDE, but I wasn't able to get the python program to parse them.

### Usage

To use the parser from terminal, run the file like you would with any standard python file (i.e. ```python3 highlight-bash.py```).
You will then be prompted in the terminal to type in a command. This will be the bash script that you would like to be parsed and highlighted.
The highlighted script will then be printed out to the terminal.


### Example Scripts

cat "file.txt" | sort | uniq -c

mkdir mydir | cd mydir | vi "myfile.txt"

ls -l | sort

cat "../path/to/file.txt/" | grep "bash"

gcc "test.cpp" -o "test"

find "/path/to/file" -type f -mtime -print

cat "path/to/file.txt" | tr "[:upper:]" "[:lower:]" | sort | uniq -c | head -n 5
