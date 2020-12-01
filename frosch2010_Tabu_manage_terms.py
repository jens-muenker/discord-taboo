import os
import json

import frosch2010_Tabu_variables as fTV
import frosch2010_Console_Utils as fCU

#-----------------------------------------------------

def load_terms(tabuVars, file_path=None):

    fCU.log_In_Console("Try to load terms...", "LOAD-TERMS", "inf")

    if not file_path:

        file_path = "tabu-terms.txt"


    if os.path.isfile(file_path):

        with open(file_path, encoding="UTF-8") as json_file:

            data = json.load(json_file)
            json_term_list = data["Term-List"].items()
            json_term_pool = data["Term-Pool"].items()

            for key, value in json_term_list:
                tabuVars.tabu_card_list.append(key + ":" + value)

            for key, value in json_term_pool:
                tabuVars.tabu_card_pool.append(key + ":" + value)

        fCU.log_In_Console("{} terms loaded in deck.".format(str(len(tabuVars.tabu_card_list))), "LOAD-TERMS", "inf")
        fCU.log_In_Console("{} terms loaded in pool.".format(str(len(tabuVars.tabu_card_pool))), "LOAD-TERMS", "inf")

    else:

        fCU.log_In_Console("No terms-file found! Load terms from channel before you start playing.", "LOAD-TERMS", "war")


def save_terms(tabuVars, file_path=None):

    fCU.log_In_Console("Try to save terms...", "SAVE-TERMS", "inf")

    if not file_path:

        file_path = "tabu-terms.txt"


    fCU.log_In_Console("Saving deck and pool...", "SAVE-TERMS", "inf")

    data = {}
    data["Term-List"] = {}
    data["Term-Pool"] = {}

    for str_Term in tabuVars.tabu_card_list:

        term_array = str_Term.split(":")

        data["Term-List"][term_array[0]] = term_array[1]


    for str_Term in tabuVars.tabu_card_pool:

        term_array = str_Term.split(":")

        data["Term-Pool"][term_array[0]] = term_array[1]


    with open(file_path, "w", encoding="UTF-8") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True, ensure_ascii=False)

    fCU.log_In_Console("Terms sucessfully saved.", "SAVE-TERMS", "inf")