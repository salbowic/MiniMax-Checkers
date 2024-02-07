import pandas as pd
from test import Test


def main():
    '''
    Different tests for playing with ai, watching ai vs ai or saving results
    of various combinations of depth and evaluation functions.
    '''
    
    Test.play_against_ai(True, 4)

    #print(Test.ai_vs_ai_visualisation(1,5))

    # print(Test.depth(5,2))

    #Test.save_depth_results(1, 6, 4)

    # Test.save_eval_results()

if __name__ == "__main__":
    main()    
    