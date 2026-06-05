# ============================================
# CREATE PLAYSTORE PLAN
# ============================================

def create_playstore_plan(app_name):

    plan = [

        {
            "action": "open_playstore",
            "target": "Play Store"
        },

        {
            "action": "tap_bottom_search",
            "target": "bottom_search"
        },

        {
            "action": "tap_top_search",
            "target": "top_search_field"
        },

        {
            "action": "type_app_name",
            "target": app_name
        },

        {
            "action": "press_enter",
            "target": "enter"
        },

        {
            "action": "open_app_page",
            "target": app_name
        },

        {
            "action": "tap_install",
            "target": "Install"
        }
    ]

    return plan