class tabu_variables:

    tabu_player_list_all = []
    tabu_player_list_team_1 = []
    tabu_player_list_team_2 = []

    tabu_points_team_1 = 0
    tabu_points_team_2 = 0

    tabu_points_history_team_1 = [0]
    tabu_points_history_team_2 = [0]
    tabu_points_this_round = 0

    tabu_guessing_team_num = 0
    tabu_explainer_team_1 = 0
    tabu_explainer_team_2 = 0

    tabu_guessing_card_messages = []
    tabu_time_messages = []

    tabu_card_list = []
    tabu_card_pool = []

    lst_Terms_already_loaded = []

    tabu_current_time = 60

    tabu_is_running = False
    tabu_is_pause = False
    tabu_is_switching = False
    tabu_is_raeacting = False

    tabu_points_to_win = 200

    tabu_edit_term_list = {}
    tabu_edit_messages_list = {}
    tabu_edit_word_list = {}
    tabu_edit_delete_card_list = {}
    tabu_edit_delete_word_list = {}


    tabu_player_list_last_game = []
    tabu_revenge_msgs = []
    tabu_revenge_player_yes = []
    tabu_revenge_asking_player_msg = None

    tabu_last_points_to_win = 0
    tabu_revenge_question = False
    tabu_revenge_time = 30


    tabu_start_team_num = 0
    tabu_is_chance = False
    tabu_was_chance = False
    tabu_chance_team = 1