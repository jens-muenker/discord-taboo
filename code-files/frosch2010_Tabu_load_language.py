import os
import sys
import json

import frosch2010_Console_Utils as fCU

def load_language(tabuLanguage, file_path=None):

    fCU.log_In_Console("Try to load language-file...", "LOAD-LANGUAGE", "inf")

    if not file_path:

        file_path = sys.argv[0].replace(os.path.basename(sys.argv[0]), "") + "tabu-language.txt"

    
    if os.path.isfile(file_path):

        with open(file_path, encoding="UTF-8") as json_file:

            try:

                data = json.load(json_file)

            except Exception as error:

                fCU.log_In_Console("Failed to load language-file!", "LOAD-LANGUAGE", "err")
                fCU.log_In_Console(str(error), "LOAD-LANGUAGE", "err")

                exit()


            try:

                tabuLanguage.tabu_wrong_arguments = str(data["Phrases"]["tabu_wrong_arguments"])

                tabuLanguage.tabu_game_already_running = str(data["Phrases"]["tabu_game_already_running"])
                tabuLanguage.tabu_no_game_running = str(data["Phrases"]["tabu_no_game_running"])

                tabuLanguage.tabu_more_players_needed = str(data["Phrases"]["tabu_more_players_needed"])
                tabuLanguage.tabu_user_already_joined = str(data["Phrases"]["tabu_user_already_joined"])
                tabuLanguage.tabu_user_joined_game = str(data["Phrases"]["tabu_user_joined_game"])
                tabuLanguage.tabu_user_started_game = str(data["Phrases"]["tabu_user_started_game"])

                tabuLanguage.tabu_game_paused_by = str(data["Phrases"]["tabu_game_paused_by"])
                tabuLanguage.tabu_game_already_paused = str(data["Phrases"]["tabu_game_already_paused"])
                tabuLanguage.tabu_game_unpaused_by = str(data["Phrases"]["tabu_game_unpaused_by"])
                tabuLanguage.tabu_game_is_not_paused = str(data["Phrases"]["tabu_game_is_not_paused"])

                tabuLanguage.tabu_search_for_new_terms = str(data["Phrases"]["tabu_search_for_new_terms"])
                tabuLanguage.tabu_search_for_new_terms_finished = str(data["Phrases"]["tabu_search_for_new_terms_finished"])

                tabuLanguage.tabu_false_term_format = str(data["Phrases"]["tabu_false_term_format"])

                tabuLanguage.tabu_save = str(data["Phrases"]["tabu_save"])

                tabuLanguage.tabu_time_left = str(data["Phrases"]["tabu_time_left"])
                tabuLanguage.tabu_time_is_up = str(data["Phrases"]["tabu_time_is_up"])
                tabuLanguage.tabu_it_will_start_soon = str(data["Phrases"]["tabu_it_will_start_soon"])
                tabuLanguage.tabu_it_will_start_in = str(data["Phrases"]["tabu_it_will_start_in"])
                tabuLanguage.tabu_game_paused = str(data["Phrases"]["tabu_game_paused"])

                tabuLanguage.tabu_team_1_won = str(data["Phrases"]["tabu_team_1_won"])
                tabuLanguage.tabu_team_2_won = str(data["Phrases"]["tabu_team_2_won"])

                tabuLanguage.tabu_card_term_prefix = str(data["Phrases"]["tabu_card_term_prefix"])
                tabuLanguage.tabu_card_term_suffix = str(data["Phrases"]["tabu_card_term_suffix"])

                tabuLanguage.tabu_graph_points = str(data["Phrases"]["tabu_graph_points"])
                tabuLanguage.tabu_graph_points_per_round = str(data["Phrases"]["tabu_graph_points_per_round"])
                tabuLanguage.tabu_graph_round = str(data["Phrases"]["tabu_graph_round"])

                tabuLanguage.tabu_game_cant_stopped = str(data["Phrases"]["tabu_game_cant_stopped"])
                tabuLanguage.tabu_game_stopped_by = str(data["Phrases"]["tabu_game_stopped_by"])

                tabuLanguage.tabu_no_kick_user = str(data["Phrases"]["tabu_no_kick_user"])
                tabuLanguage.tabu_kick_user_isnt_player = str(data["Phrases"]["tabu_kick_user_isnt_player"])
                tabuLanguage.tabu_cant_kick_current_explainer = str(data["Phrases"]["tabu_cant_kick_current_explainer"])
                tabuLanguage.tabu_user_kicked = str(data["Phrases"]["tabu_user_kicked"])

                tabuLanguage.tabu_shutdown_bot = str(data["Phrases"]["tabu_shutdown_bot"])

            except Exception as error:

                fCU.log_In_Console("Failed to load language-file!", "LOAD-LANGUAGE", "err")
                fCU.log_In_Console(str(error), "LOAD-LANGUAGE", "err")
                fCU.log_In_Console("Shutdown bot. Please check the language-file for errors.", "LOAD-LANGUAGE", "inf")

                exit()

            fCU.log_In_Console("Language-file successfully loaded.", "LOAD-LANGUAGE", "inf")
    else:

        fCU.log_In_Console("No language-file found...", "LOAD-LANGUAGE", "err")
        fCU.log_In_Console("Shutdown bot. Please configure the bot.", "LOAD-LANGUAGE", "inf")

        exit()