import subprocess
import random
import os
import contextlib
import shutil

def clear_dir(dire):
    try:
        shutil.rmtree(dire)
    except OSError:
        pass

def clear_files(files):
    with contextlib.suppress(FileNotFoundError):
        for file in files:
            os.remove(file)


def compile_cpp(cpp, binary, safe=False):
    compilation_process = 1
    if safe:
        compilation_process = subprocess.run(
            ['g++', '-std=c++17', '-Wshadow', '-Wall', '-o', binary, cpp, '-g', '-fsanitize=address','-fsanitize=undefined', '-D_GLIBCXX_DEBUG'],
            capture_output=True,
            text=True,
            check=False)
    else:
        compilation_process = subprocess.run(
            ['g++', '-o', binary, cpp],
            capture_output=True,
            text=True,
            check=False)
    if compilation_process.returncode != 0:
        return 1
    return 0


#    Return Values:
#       0 All test passed
#       1 Generator's execution failed 
#       2 Correct solution's execution failed
#       3 Wrong solution's execution failed
#       4 Wrong soultion exceeded the time limit
#       5 Wrong output produced
#       6 Another worker already finished

def worker(name, test_cases, time_limit):
    current_folder = 'files/worker' + str(name) + '/'
    subprocess.call(['mkdir', '-p', current_folder])
    subprocess.call(['cp', '-t', current_folder, 'gen', 'checker', 'wrong', 'correct'])
    for _ in range(test_cases):

        # Run generator
        seed = random.randint(1, 1000000000)
        with open(current_folder + 'input.txt', 'w+', encoding='utf-8') as output_file, open('log.txt', 'w+', encoding='utf-8') as err_file:
            gen_execution = subprocess.run([current_folder + 'gen', str(seed)], stdout=output_file, stderr=err_file, check=False)
        if gen_execution.returncode != 0:
            return 1

        # Run correct solution
        with open(current_folder + 'input.txt', 'r', encoding='utf-8') as input_file, \
                open(current_folder + 'correct_output.txt', 'w+', encoding='utf-8') as output_file, \
                open('log.txt', 'w+', encoding='utf-8') as err_file:
            correct_execution = subprocess.run(current_folder + 'correct', stdin=input_file, stdout=output_file, stderr=err_file, text=True, check=False)
        if correct_execution.returncode != 0:
            return 2 

        # Run wrong solution
        try:
            with open(current_folder + 'input.txt', 'r', encoding='utf-8') as input_file, \
                    open(current_folder + 'wrong_output.txt', 'w+', encoding='utf-8') as output_file, \
                    open('log.txt', 'w+', encoding='utf-8') as err_file:
                wrong_solution = subprocess.run(current_folder + 'wrong', stdin=input_file, 
                        stdout=output_file, stderr=err_file, text=True, timeout=time_limit, check=False)
            if wrong_solution.returncode != 0:
                return 3
        except subprocess.TimeoutExpired:
            clear_dir('results')
            subprocess.call(['mkdir', '-p', 'results'])
            subprocess.call(['cp', current_folder + 'input.txt', 'results/'])
            subprocess.call(['cp', current_folder + 'correct_output.txt', 'results/'])
            return 4

        # Run checker
        check_execution = subprocess.run([current_folder + 'checker', current_folder + 'correct_output.txt', current_folder + 'wrong_output.txt'], check=False)
        if check_execution.returncode != 0:
            clear_dir('results')
            subprocess.call(['mkdir', '-p', 'results'])
            subprocess.call(['cp', current_folder + 'input.txt', 'results/'])
            subprocess.call(['cp', current_folder + 'correct_output.txt', 'results/'])
            subprocess.call(['cp', current_folder + 'wrong_output.txt', 'results/'])
            return 5
    return 0

def execute(test_cases, time_limit):
    clear_dir('results')
    clear_files(['log.txt'])
    workers = 1
    results = [worker(1, test_cases, time_limit)]
    clear_files(['wrong', 'gen', 'checker', 'correct'])
    clear_dir('files')
    # No counter example founded
    if results == [0 for i in range(workers)]:
        return 0
    for i in range(workers):
        if results[i] < 6:
            return results[i]
    return -1  

def compile_files(safe):
    if compile_cpp('generator.cpp', 'gen', False) != 0:
        return 1
    if compile_cpp('checker.cpp', 'checker', False) != 0:
        return 2
    if compile_cpp('wrong.cpp', 'wrong', safe) != 0:
        return 3
    if compile_cpp('correct.cpp', 'correct', False) != 0:
        return 4
    return 0


#    Return value:
#        0 All test passed
#        1 Generator's compilation failed
#        2 Checker's compilation failed
#        3 Wrong solution's compilation failed
#        4 Correct solution's compilation failed
#        5 Generator's execution failed 
#        6 Correct solution's execution failed
#        7 Wrong solution's execution failed
#        8 Wrong soultion exceeded the time limit
#        9 Wrong output produced

def stresstest(safe, tcs, tl):
    clear_files(['log.txt'])
    compilation = compile_files(safe)
    if compilation != 0:
        return compilation
    execution = execute(tcs, tl)
    if execution != 0:
        execution += 4
    return execution


def main():
    return stresstest(False, 100, 1)


if __name__ == '__main__':
    main()
