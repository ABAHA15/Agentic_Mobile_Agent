# ============================================
# CREATE YOUTUBE PLAN
# ============================================

def create_youtube_plan(query):

    return [

        {
            "action": "open_youtube",
            "target": "youtube"
        },

        {
            "action": "tap_search_icon",
            "target": "search_icon"
        },

        {
            "action": "type_query",
            "target": query
        },

        {
            "action": "press_enter",
            "target": "enter"
        },

        {
            "action": "open_first_reel",
            "target": "first_reel"
        },

        {
            "action": "watch_reel",
            "target": "reel_1"
        },

        {
            "action": "swipe_next",
            "target": "next_reel"
        },

        {
            "action": "watch_reel",
            "target": "reel_2"
        },

        {
            "action": "swipe_next",
            "target": "next_reel"
        },

        {
            "action": "watch_reel",
            "target": "reel_3"
        }
    ]