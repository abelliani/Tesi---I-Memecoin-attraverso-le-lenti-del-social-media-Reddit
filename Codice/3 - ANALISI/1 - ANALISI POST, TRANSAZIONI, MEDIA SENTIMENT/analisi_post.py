import pandas as pd
from datetime import datetime

# Carichiamo più file JSON di post
post_files = ["combined_posts_sorted.json"]
posts_df_list = [pd.read_json(file, orient="records") for file in post_files]
posts_df = pd.concat(posts_df_list, ignore_index=True)

# Carichiamo più file JSON di commenti
comment_files = ["combined_comments_sorted.json"]
comments_df_list = [pd.read_json(file, orient="records") for file in comment_files]
comments_df = pd.concat(comments_df_list, ignore_index=True)

# Convertiamo il campo 'created_utc' da Unix a data per entrambe le tabelle
posts_df['date'] = pd.to_datetime(posts_df['created_utc'], unit='s').dt.date
comments_df['date'] = pd.to_datetime(comments_df['created_utc'], unit='s').dt.date

# Aggiungi settimana e mese per i post e i commenti
posts_df['week_year'] = posts_df['date'].apply(lambda x: x.strftime('%Y-%U'))  # Format: 'YYYY-WW'
posts_df['month_year'] = posts_df['date'].apply(lambda x: x.strftime('%Y-%m'))  # Format: 'YYYY-MM'
comments_df['week_year'] = comments_df['date'].apply(lambda x: x.strftime('%Y-%U'))  # Format: 'YYYY-WW'
comments_df['month_year'] = comments_df['date'].apply(lambda x: x.strftime('%Y-%m'))  # Format: 'YYYY-MM'

# 1. Conteggio totale di post per giorno, suddiviso per subreddit
posts_per_day_subreddit = posts_df.groupby(['date', 'subreddit']).size().reset_index(name='total_posts_per_day')
posts_per_day_subreddit['date'] = pd.to_datetime(posts_per_day_subreddit['date']).dt.strftime('%Y-%m-%d')

# 2. Conteggio totale di post per giorno (Totale senza differenziazione per subreddit)
posts_per_day_total = posts_df.groupby('date').size().reset_index(name='total_posts_per_day')
posts_per_day_total['date'] = pd.to_datetime(posts_per_day_total['date']).dt.strftime('%Y-%m-%d')

# 3. Conteggio totale di post per settimana, suddiviso per subreddit
posts_per_week_subreddit = posts_df.groupby(['week_year', 'subreddit']).size().reset_index(name='total_posts_per_week')

# 4. Conteggio totale di post per settimana (Totale senza differenziazione per subreddit)
#posts_per_week_total = posts_df.groupby('week_year').size().reset_index(name='total_posts_per_week')

# 5. Conteggio totale di post per mese, suddiviso per subreddit
#posts_per_month_subreddit = posts_df.groupby(['month_year', 'subreddit']).size().reset_index(name='total_posts_per_month')

# 6. Conteggio totale di post per mese (Totale senza differenziazione per subreddit)
#posts_per_month_total = posts_df.groupby('month_year').size().reset_index(name='total_posts_per_month')

# 7. Conteggio dei post per subreddit
#posts_per_subreddit = posts_df.groupby('subreddit').size().reset_index(name='total_posts_per_subreddit')

# 8. Conteggio totale di post (senza suddivisione per subreddit)
total_posts = posts_df.shape[0]

# 9. Post con maggiore engagement (numero di commenti)
# comments_count = comments_df.groupby('link_id').size().reset_index(name='total_comments')
# posts_df['link_id'] = 't3_' + posts_df['id']
# post_engagement = posts_df.merge(comments_count, left_on='link_id', right_on='link_id', how='left').fillna(0)
# post_engagement['total_comments'] = post_engagement['total_comments'].astype(int)
# top_engagement_posts = post_engagement.nlargest(10, 'total_comments')[['title', 'total_comments']]

# 10. Tempo medio di creazione dei post
posts_df['creation_time'] = pd.to_datetime(posts_df['created_utc'], unit='s')
posts_df['time_diff'] = (posts_df['creation_time'] - posts_df['creation_time'].min()).dt.days
average_post_time = posts_df['time_diff'].mean()

# 11. Risultati dei post
post_results = {
    "posts_per_day": posts_per_day_total.to_dict(orient='records'),
    "posts_per_day_subreddit": posts_per_day_subreddit.to_dict(orient='records'),
    #"posts_per_week": posts_per_week_total.to_dict(orient='records'),
    "posts_per_week_subreddit": posts_per_week_subreddit.to_dict(orient='records'),
    #"posts_per_month": posts_per_month_total.to_dict(orient='records'),
    #"posts_per_month_subreddit": posts_per_month_subreddit.to_dict(orient='records'),
    #"posts_per_subreddit": posts_per_subreddit.to_dict(orient='records'),
    "total_posts": total_posts,
    #"top_engagement_posts": top_engagement_posts.to_dict(orient='records'),
    "average_post_time": average_post_time
}

# 12. Commenti per giorno, suddivisi per subreddit
comments_per_day_subreddit = comments_df.groupby(['date', 'subreddit']).size().reset_index(name='total_comments_per_day')
comments_per_day_subreddit['date'] = pd.to_datetime(comments_per_day_subreddit['date']).dt.strftime('%Y-%m-%d')

# 13. Commenti per giorno (Totale senza suddivisione per subreddit)
comments_per_day_total = comments_df.groupby('date').size().reset_index(name='total_comments_per_day')
comments_per_day_total['date'] = pd.to_datetime(comments_per_day_total['date']).dt.strftime('%Y-%m-%d')

# 14. Commenti per settimana
comments_per_week = comments_df.groupby('week_year').size().reset_index(name='total_comments_per_week')

# 15. Commenti per mese
#comments_per_month = comments_df.groupby('month_year').size().reset_index(name='total_comments_per_month')

# 16. Commenti per post
#comments_per_post = comments_df.groupby('link_id').size().reset_index(name='total_comments_per_post')

# 17. Commenti per utente
#total_comments_per_user = comments_df.groupby('author').size().reset_index(name='total_comments')

# 18. Commenti con maggiore punteggio
#top_engagement_comments = comments_df.nlargest(10, 'score')[['body', 'score']]

# 19. Distribuzione dei commenti
comments_distribution = comments_df.groupby('parent_id').size().reset_index(name='total_comments_by_parent')

# 20. Risultati dei commenti
comment_results = {
    "comments_per_day": comments_per_day_total.to_dict(orient='records'),
    "comments_per_day_subreddit": comments_per_day_subreddit.to_dict(orient='records'),
    "comments_per_week": comments_per_week.to_dict(orient='records'),
    #"comments_per_month": comments_per_month.to_dict(orient='records'),
    #"comments_per_post": comments_per_post.to_dict(orient='records'),
    #"total_comments_per_user": total_comments_per_user.to_dict(orient='records'),
    #"top_engagement_comments": top_engagement_comments.to_dict(orient='records'),
    "comments_distribution": comments_distribution.to_dict(orient='records')
}

# 21. Statistiche dei post e commenti per utente
# user_stats = []
# unique_authors = set(posts_df['author'].tolist() + comments_df['author'].tolist())

# for author in unique_authors:
#     total_posts = posts_df[posts_df['author'] == author].shape[0]
#     total_comments = comments_df[comments_df['author'] == author].shape[0]
#     daily_posts = total_posts / (len(posts_per_day_total) or 1)
#     daily_comments = total_comments / (len(comments_per_day_total) or 1)
    
#     user_stats.append({
#         "author": author,
#         "total_posts": total_posts,
#         "average_daily_posts": daily_posts,
#         "total_comments": total_comments,
#         "average_daily_comments": daily_comments
#     })

# # 22. Statistiche degli utenti
# user_stats_result = {
#     "users": user_stats
# }

# 23. Statistiche dei commenti per post
# post_comment_stats = []
# for post_id in posts_df['id']:
#     post_comments = comments_df[comments_df['link_id'] == f"t3_{post_id}"]
#     total_comments = post_comments.shape[0]
    
#     comments_per_day = post_comments.groupby('date').size().to_dict()
#     comments_per_day = {date.strftime('%Y-%m-%d'): count for date, count in comments_per_day.items()}
    
#     post_comment_stats.append({
#         "post_id": post_id,
#         "total_comments": total_comments,
#         "comments_per_day": comments_per_day
#     })

# 24. Salviamo i risultati in formato JSON
pd.Series(post_results).to_json("post_results.json", orient="index", indent=4)
pd.Series(comment_results).to_json("comment_results.json", orient="index", indent=4)
# pd.Series(user_stats_result).to_json("user_stats.json", orient="index", indent=4)
# pd.Series({"posts": post_comment_stats}).to_json("post_comment_stats.json", orient="index", indent=4)

print("Risultati salvati in 'post_results.json', 'comment_results.json', 'user_stats.json', e 'post_comment_stats.json'")
