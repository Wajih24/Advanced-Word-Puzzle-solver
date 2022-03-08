import csv
import argparse
from termcolor import colored

class Puzzle:
    def __init__(self, puzzle , words):
        self.puzzle = self.parse_puzzle(puzzle)
        self.words = self.parse_words(words)
        self.solved = []

    def parse_puzzle(self, puzzle_name):
        puzzle = []
        with open(puzzle_name, 'r') as pfile:
            p_reader = ((pfile.read()).upper()).split('\n')
            for p_row in p_reader:
                puzzle.append([p_row])
            
        return puzzle
    
    def parse_words(self, list_name):
        words = []
        with open(list_name, 'r') as cfile:
            c_reader = ((cfile.read()).upper()).split('\n')
            for c_row in c_reader:
                words.append((c_row.upper()).replace(' ', '')) 
            
        return words 

    def output_cli(self):
        for ri, row in enumerate(self.puzzle):
            for chi, ch in enumerate(row[0]):
                if (ri, chi) in self.solved:
                    print(colored(f"{ch}", "green"),end=" ")
                else:
                    print(colored(f"{ch}", "blue"),end=" ")
            print()

    def find_word(self):
        for word in self.words:
            try :
                if self.find_horizontal(word):
                    continue
            except :
                pass
            try :
                if self.find_vertical(word):
                    continue
            except :
                pass
            try :
                if self.find_diagonal(word):
                    continue
            except :
                pass

    def find_horizontal(self, word):
        for ri, row in enumerate(self.puzzle):
            if word in str(row):
                for i in range(0, len(word)):
                    self.solved.append((ri, str(row).find(word) - 2 + i))
                return True
            row_r = str(row)[::-1]
            if word in row_r:
                for i in range(0, len(word)):
                    self.solved.append((ri, len(row_r) - str(row_r).find(word) - 3 - i))
                return True
        return False

    def find_vertical(self, word):
        for char in range(len(self.puzzle[0][0])):
            temp = []
            try :
                for col in range(len(self.puzzle)):
                    temp.append(self.puzzle[col][0][char])
            except :
                pass
            temp = ''.join(temp)
            temp_r = temp[::-1]
            if word in str(temp):
                for i in range(0, len(word)):
                    self.solved.append((str(temp).find(word) + i, char))
                return True
            if word in str(temp_r):
                for i in range(0, len(word)):
                    self.solved.append((len(temp_r) - str(temp_r).find(word) - 1 - i, char))
                return True
        return False

    def find_diagonal(self, word):
        for a in range(0, len(self.puzzle[0][0])):
            temp = [[] for i in range(8)]
            ranges = [[] for i in range(8)]
            i = 0
            while ((a - i) >= 0) and (i < len(self.puzzle)):
                coords = [[i, a-i],[29-i, a-i], [29-i, 29-(a-i)], [i, 29-(a-i)]]
                for cx, c in enumerate(coords):
                    temp[cx].append(self.puzzle[c[0]][0][c[1]])
                    ranges[cx].append((c[0], c[1]))
                    ranges[cx+4].append((c[1], c[0]))
                i+=1

            for ti in range(4):
                temp[ti] = ''.join(temp[ti])
                temp[ti+4] = temp[ti][::-1]

            for tx, t in enumerate(temp):
                if word in str(t):
                    for i in range(0, len(word)):
                        self.solved.append(ranges[tx][str(t).find(word) + i])
                    return True
        return False
            
    

if __name__ == "__main__":
    puzzle="output/final.txt"
    words="words.txt"
    p = Puzzle(puzzle,words)
    print("\nPROBLEM:")
    p.output_cli()
    print("\nSOLUTION:")
    p.find_word()
    p.output_cli()

