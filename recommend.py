import map_classification as mc


def recommend_player(player_id, class_id):
    # print()
    # print(f"Getting map recommendations for player {player_id}, class {'soldier' if class_id == 3 else 'demo'}")
    # print()
    mc.load_model(class_id)
    tts = mc.get_player_tts(player_id, class_id)

    if len(tts) == 0:
        return None

    # group map names into lists by rank
    groups = {}
    for time in tts:
        if str(time["rank"]) not in groups:
            groups[str(time["rank"])] = {"multiplier": 1 / time["rank"], "names": []}

        groups[str(time["rank"])]["names"].append(time["map_name"])

    # get recommendations and apply weight
    recommendations = {}
    for key, group in groups.items():
        similar = mc.get_similar(group["names"], 0)
        for s in similar:
            # Scale maps where player already has tt down, so that
            # #10 = 0.9, #9 = 0.8, ..., wr = 0.0
            for time in tts:
                if s["name"] == time["map_name"]:
                    s["value"] *= (time["rank"] - 1) / 10
                    break

            s["value"] *= group["multiplier"]

            if s["name"] in recommendations:
                recommendations[s["name"]] += s["value"]
            else:
                recommendations[s["name"]] = s["value"]

    recommendations_list = []
    for k, v in recommendations.items():
        recommendations_list.append({"name": k, "value": v})
    recommendations_list.sort(key=lambda r: -r["value"])
    return recommendations_list
