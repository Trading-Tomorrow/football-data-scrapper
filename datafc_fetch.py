from datafc import match_data, match_stats_data
import pandas as pd

TOURNAMENT_ID = 17  # Premier League (SofaScore unique-tournament id; adjust if needed)
SEASON_ID = 61627  # 2022/23 season id on SofaScore; adjust if needed
DATA_SOURCE = "sofascore"
START_WEEK = 1
MAX_WEEKS_TO_SCAN = 38  # safety upper bound
MAX_CONSECUTIVE_EMPTY = 3  # stop if this many weeks in a row return no events


def main():
    print("Fetching matches for the 2022/23 season...")

    all_match_frames = []
    empty_streak = 0
    for week in range(START_WEEK, MAX_WEEKS_TO_SCAN + 1):
        try:
            week_df = match_data(
                tournament_id=TOURNAMENT_ID,
                season_id=SEASON_ID,
                week_number=week,
                data_source=DATA_SOURCE,
                enable_json_export=False,
                enable_excel_export=False,
            )
        except RuntimeError as exc:
            msg = str(exc)
            if "Invalid API response format: 'events' key is missing" in msg or "No match data found" in msg:
                print(f"Week {week}: no events returned (message: {msg}). Skipping.")
                empty_streak += 1
                if empty_streak >= MAX_CONSECUTIVE_EMPTY:
                    print("Stopping scan after consecutive empty weeks. Adjust IDs if this happens from week 1.")
                    break
                continue
            raise
        except Exception as exc:
            print(f"Week {week}: error fetching data ({exc}).")
            empty_streak += 1
            if empty_streak >= MAX_CONSECUTIVE_EMPTY:
                print("Stopping scan after repeated errors. Verify Chrome/Selenium setup or IDs.")
                break
            continue

        empty_streak = 0
        all_match_frames.append(week_df)
        print(f"Week {week}: {len(week_df)} matches")

    if not all_match_frames:
        raise SystemExit("No match data fetched. Check tournament_id/season_id or data_source.")

    match_df = pd.concat(all_match_frames, ignore_index=True)
    print(f"Total matches collected: {len(match_df)}")
    print(match_df.head())

    print("Fetching detailed stats for each match...")
    try:
        stats_df = match_stats_data(
            match_df=match_df,
            data_source=DATA_SOURCE,
            enable_json_export=False,
            enable_excel_export=False,
        )
    except RuntimeError as exc:
        raise SystemExit(f"Failed to fetch match stats: {exc}")

    if stats_df.empty:
        raise SystemExit("Match stats response is empty.")

    print(f"Total stat rows: {len(stats_df)}")
    print(stats_df.head())

    # Normalize id column names
    match_df = match_df.copy()
    match_df["match_id"] = match_df.get("match_id", match_df.get("game_id"))

    stats_df = stats_df.copy()
    stats_df["match_id"] = stats_df.get("match_id", stats_df.get("game_id"))

    if stats_df["match_id"].isna().any():
        raise SystemExit("Stats data missing match/game id; cannot pivot.")

    # Wide-format stats with team prefixes
    stats_wide_df = stats_df.pivot_table(
        index="match_id",
        columns="stat_name",
        values=["home_team_stat", "away_team_stat"],
        aggfunc="first",  # avoid numeric averaging on string stats
    )
    stats_wide_df.columns = [f"{team}_{stat}" for team, stat in stats_wide_df.columns]
    stats_wide_df.reset_index(inplace=True)

    # Join schedule with wide stats
    full_df = match_df.merge(stats_wide_df, on="match_id", how="left")

    # Save CSV
    output_path = "premierleague_2024_25_stats.csv"
    full_df.to_csv(output_path, index=False)
    print(f"CSV saved: {output_path}")

    # Example: possession snapshot
    possession_cols = [c for c in full_df.columns if "possession" in c.lower()]
    if possession_cols:
        base_cols = ["match_id", "home_team", "away_team"]
        possession_df = full_df[base_cols + possession_cols]
        print("Possession overview:")
        print(possession_df.head())
    else:
        print("Possession columns not found in stats; check stat names in the CSV.")


if __name__ == "__main__":
    main()
