library("tidyr")
library("ggplot2")
library("ggbeeswarm")
library("hms")
library("RColorBrewer")
library("dplyr")
library('lubridate')

## Table for URL shorteners 

df <- read.csv('../dataset/final_dataset_output.csv')

shortened_data <- subset(df, url_shortener != "")

shortened_data <- subset(shortened_data, scam_type != "spam")

summary <- shortened_data %>%
    group_by(scam_type, url_shortener) %>%
    summarise(count = n(), .groups = "drop") %>%
    arrange(desc(count))

table(shortened_data$scam_type, shortened_data$url_shortener)

## Reproduce Figure 2

timestamps<-read.csv('../dataset/time_day.csv', header=FALSE)

timestamps$V2<-format(timestamps$V2,format='%H:%M:%S')
timestamps$V2<-as_hms(timestamps$V2)
matches<-which(timestamps$V1 =='Tuesday' & as.character(timestamps$V2) == '11:34:00')
rows_to_remove <- matches[-(1:7)]
timestamps_without_india_camp <- timestamps[-rows_to_remove, ]

incoming_msgs_weekday<-factor(timestamps_without_india_camp$V1, levels=c('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'))

par(mar = c(7,7,1,1), mgp = c(5, 1, 0))

dotplot <- timestamps_without_india_camp %>%
    ggplot(aes(x = incoming_msgs_weekday, y = timestamps_without_india_camp$V2)) +
    ggbeeswarm::geom_quasirandom(
        shape = 21, color = "white",
        alpha = 0.8, size = 3,
        aes(fill = incoming_msgs_weekday)
    ) +
    scale_fill_manual(values = brewer.pal(8, "Accent")[1:7]) +
    labs(x = "Days of the Week", y = "Time of the Day when Smish Received")  +
    theme(axis.text=element_text(size=15), axis.title=element_text(size=14))

dotplot 

group1 <- timestamps[timestamps$V1=="Monday",]
group2 <- timestamps[timestamps$V1=="Tuesday",]
group3 <- timestamps[timestamps$V1=="Wednesday",]
group4 <- timestamps[timestamps$V1=="Thursday",]
group5 <- timestamps[timestamps$V1=="Friday",]  
group6 <- timestamps[timestamps$V1=="Saturday",]  
group7 <- timestamps[timestamps$V1=="Sunday",]  

# KS Test
group1$incoming_msgs_hms<-lubridate::hms(group1$V2)
group1$secs<-period_to_seconds(group1$incoming_msgs_hms)
group2$incoming_msgs_hms<-lubridate::hms(group2$V2)
group2$secs<-period_to_seconds(group2$incoming_msgs_hms)
group3$incoming_msgs_hms<-lubridate::hms(group3$V2)
group3$secs<-period_to_seconds(group3$incoming_msgs_hms)
group4$incoming_msgs_hms<-lubridate::hms(group4$V2)
group4$secs<-period_to_seconds(group4$incoming_msgs_hms)
group5$incoming_msgs_hms<-lubridate::hms(group5$V2)
group5$secs<-period_to_seconds(group5$incoming_msgs_hms)
group6$incoming_msgs_hms<-lubridate::hms(group6$V2)
group6$secs<-period_to_seconds(group6$incoming_msgs_hms)
group7$incoming_msgs_hms<-lubridate::hms(group7$V2)
group7$secs<-period_to_seconds(group7$incoming_msgs_hms)
ks.test(group1$secs,group2$secs)

## Reproduce Figure 3

df <- read.csv('../dataset/final_dataset_output.csv')

shortened_data <- subset(df, original_network_country != "")

shortened_data <- subset(shortened_data, scam_type != "spam")
shortened_data <- subset(shortened_data, scam_type != "")

summary <- shortened_data %>%
    group_by(scam_type, original_network_country) %>%
    summarise(count = n(), .groups = "drop") %>%
    arrange(desc(count))


selected_countries <- c("IND", "USA", "AUS", "GBR", "NLD","ESP","FRA","BEL","DEU","IDN")

df_clean <- summary %>%
    filter(original_network_country %in% selected_countries) %>%
    group_by(original_network_country, scam_type) %>%
    summarise(count = sum(count, na.rm = TRUE), .groups = "drop") %>%
    group_by(original_network_country) %>%
    mutate(percent = count / sum(count) * 100) %>%
    ungroup() %>%
    mutate(country = factor(original_network_country, levels = selected_countries, ordered = TRUE))

df_clean$original_network_country <- factor(df_clean$original_network_country, levels = c("IND", "USA", "AUS", "GBR", "NLD","ESP","FRA","BEL","DEU","IDN"))


ggplot(df_clean, aes(x = original_network_country, y = percent, fill = scam_type)) +
    geom_bar(stat = "identity", position = "stack") +
    scale_fill_brewer(palette = "Set2") +   # nice soft colors
    labs(
        x = "Countries",
        y = "Percentage of Mobile Numbers",
        fill = "Scam Type"
    ) +
    theme_minimal() +
    theme(
        axis.text.x = element_text(angle = 45, hjust = 1, size=15),
        axis.text.y = element_text(size = 15),
        axis.title.x = element_text(size = 16, face = "bold"),
        axis.title.y = element_text(size = 16, face = "bold"),
        legend.text  = element_text(size = 16),
        legend.title = element_text(size = 16)
    )
