setwd('D:\\JetBrains\\202107\\统计选讲\\Project')

library(dplyr)
library(ggplot2)
library(RColorBrewer)
library(gridExtra)
library(ggthemes)
library(bibliometrix)

data <- read.csv('data.csv', na.strings = "NA")
data <- as.data.frame(data)
data <- data[, -c(7, 8, 9)]
table(data$Document.Type)


year_data <- as.data.frame(table(data$Year))
names(year_data) <- c('Year', 'Counts')
year_mean_1 <- group_by(data[,c(7,8,9)], Year) %>% 
  summarize_each(funs(mean))
year_mean_2 <- group_by(data[which(data$Page!=0),c(9,11)], Year) %>% 
  summarize_each(funs(mean))
names(year_mean_2)[2] <- 'Pages'

year_data <- data.frame(year_data, year_mean_1[,c(2,3)], year_mean_2[,2])

set_col <- 'Set2'

p1 <- ggplot(data = year_data, aes(x = Year, y = Counts, group = 1)) + 
  geom_line(color = brewer.pal(4, set_col)[1], size = 1.2) + 
  geom_point(size=3, shape=16, color = brewer.pal(4, set_col)[1]) + theme_economist() +
  labs(title="Panel A: Trend of the Number of Publications", x="Year", y="The Number of Publications") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14),
        plot.title = element_text(hjust = 0.5, size = 14)) + 
  scale_x_discrete(breaks = c(0:9)*5+1971)

p2 <- ggplot(data = year_data, aes(x = Year, y = Citations, group = 1)) + 
  geom_line(color = brewer.pal(4, set_col)[2], size = 1.2) + 
  geom_point(size=3, shape=17, color = brewer.pal(4, set_col)[2]) + theme_economist() +
  labs(title="Panel B: Trend of the Number of Citations", x="Year", y="The Number of Citations") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14),
        plot.title = element_text(hjust = 0.5, size = 14)) + 
  scale_x_discrete(breaks = c(0:9)*5+1971)

p3 <- ggplot(data = year_data, aes(x = Year, y = Ref.Counts, group = 1)) + 
  geom_line(color = brewer.pal(4, set_col)[3], size = 1.2) + 
  geom_point(size=3, shape=18, color = brewer.pal(4, set_col)[3]) + theme_economist() +
  labs(title="Panel C: Trend of the Number of References", x="Year", y="The Number of References") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14),
        plot.title = element_text(hjust = 0.5, size = 14)) + 
  scale_x_discrete(breaks = c(0:9)*5+1971)

p4 <- ggplot(data = year_data, aes(x = Year, y = Pages, group = 1)) + 
  geom_line(color = brewer.pal(4, set_col)[4], size = 1.2) + 
  geom_point(size=3, shape=19, color = brewer.pal(4, set_col)[4]) + theme_economist() +
  labs(title="Panel D: Trend of the Number of Pages", x="Year", y="The Number of Pages") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14),
        plot.title = element_text(hjust = 0.5, size = 14)) + 
  scale_x_discrete(breaks = c(0:9)*5+1971)

grid.arrange(p1, p2, p3, p4, ncol=2)


table(data$Document.Type)

category <- strsplit(data$Category, split = ';')
n <- nrow(data)
data$Category <- rep(0, n)
for(i in 1:n){
  data$Category[i] <- category[[i]][1]
}
others <- names(sort(table(data$Category))[1:19])
data$Category[which(data$Category %in% others)] <- 'Others'

tapply(data$Citations, data$Category, mean)
tapply(data$Citations, data$Category, median)

ggplot(data=data, aes(x=Year, fill=Category)) + 
  geom_bar(position='fill') + theme_economist() + 
  theme(legend.position='right', legend.text=element_text(size=8)) + 
  scale_fill_brewer(palette = "Spectral") +
  labs(x="Year", y="Proportion") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14))



journal_temp <- data.frame(sort(table(data$Source), decreasing = TRUE)[1:15])
names(journal_temp) <- c('Source', 'Counts')
journal_list <- names(sort(table(data$Source), decreasing = TRUE)[1:15])
journal_data <- group_by(data[which(data$Source %in% journal_list), ], Source) %>% 
  summarize(Citations=mean(Citations))

journal_data <- merge(journal_data, journal_temp, by.x = "Source", all.x=TRUE)
journal_data <- journal_data[sort(journal_data$Counts, index.return=TRUE, decreasing = TRUE)$ix,]

journal_data$Source <- factor(journal_data$Source, levels = journal_data$Source)

getPalette <- colorRampPalette(brewer.pal(11, 'Spectral'))
ggplot(data = journal_data, mapping=aes(x=Source, y=Counts, fill=Source, 
                                        group=1))+
  geom_bar(stat="identity", width=0.75) + theme_economist() + 
  theme(legend.position='right', legend.text=element_text(size=8), legend.title=element_blank()) +
  labs(x="Journal") + 
  scale_x_discrete(labels = NULL)+  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14)) +
  scale_fill_manual(values = getPalette(15)) + 
  geom_point(aes(y = Citations*8), shape = 3, size = 3, color = 'black') + 
  scale_y_continuous(sec.axis = sec_axis(~. /8, name = "Average Citations")) +
  geom_text(aes(label = Counts, vjust = -0.8, hjust = 0.5), show.legend = FALSE)

sort(table(data$University), decreasing = TRUE)[1:20]
data <- data[,c(1:17,19,18,20:23)]

country_list <- names(data)[14:23]
cooperation <- matrix(rep(0,100), ncol = 10)
for(i in c(1:10)){
  for(j in c(1:10))
  cooperation[i,j] <- sum(data[,i+13] * data[,j+13])
}

cooperation_data <- data.frame(Country = country_list, Counts = diag(cooperation))
cooperation_data$Country <- factor(cooperation_data$Country, levels = cooperation_data$Country)

for(i in c(1:10)){
  cooperation[i,] <- cooperation[i,]/cooperation[i,i]
}

heat <- c()
for(i in c(1:10)){
  heat <- c(heat, cooperation[,i])
}
country2 <- c()
for(i in c(1:10)){
  country2 <- c(country2, rep(country_list[i], 10))
}

heat_data <- data.frame(country1 = rep(country_list,10), country2 = country2, Proportion = heat)

heat_data$country1 <- as.factor(heat_data$country1)
heat_data$country2 <- as.factor(heat_data$country2)

p5 <- ggplot(data = cooperation_data, mapping=aes(x=Country, y=Counts, fill=Country, 
                                        group=1))+
  geom_bar(stat="identity", width=0.75) + theme_economist() + 
  theme(legend.position='null', legend.text=element_text(size=10), legend.title=element_blank()) +
  labs(x="Country") + 
  # scale_x_discrete(labels = NULL)+  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14)) +
  scale_fill_brewer(palette = "Spectral") +
  geom_text(aes(label = Counts, vjust = -0.8, hjust = 0.5), show.legend = FALSE)


p6 <- ggplot(heat_data, aes(country2, country1)) +   
  geom_tile(aes(fill = Proportion)) +  theme_economist() +
  scale_fill_gradient(name="Proportion", low =  brewer.pal(4, 'Reds')[1], high = "red") +
  labs(x = "", y = "", title = "") + 
  theme(legend.position='right', legend.text=element_text(size=10),
        axis.text.x = element_text(angle = 45, vjust = 0.4))

grid.arrange(p5, p6, ncol=2)

nrow(data[which(data$Year > 1980 & data$Year <= 1990 & data$Keywords != ''), ])
nrow(data[which(data$Year > 1980 & data$Year <= 1990 & data$Keywords == ''), ])

nrow(data[which(data$Year > 1990 & data$Year <= 2000 & data$Keywords != ''), ])
nrow(data[which(data$Year > 1990 & data$Year <= 2000 & data$Keywords == ''), ])


polarity_data <- read.csv('./mydata/polarity data.csv', na.strings = "NA")

p7 <- ggplot(data = polarity_data, aes(x = Year, y = Polarity, group = 1)) + 
  geom_line(color = brewer.pal(6, set_col)[1], size = 1.2) + 
  geom_point(size=3, shape=18, color = brewer.pal(6, set_col)[2]) + theme_economist() +
  labs(title="Panel A: Trend of Polarity", x="Year", y="Polarity") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14),
        plot.title = element_text(hjust = 0.5, size = 14)) + 
  scale_x_continuous(breaks = c(0:5)*5+1991)

p8 <- ggplot(data = polarity_data, aes(x = Year, y = Subjectivity, group = 1)) + 
  geom_line(color = brewer.pal(6, set_col)[3], size = 1.2) + 
  geom_point(size=3, shape=19, color = brewer.pal(6, set_col)[4]) + theme_economist() +
  labs(title="Panel B: Trend of Subjectivity", x="Year", y="Subjectivity") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14),
        plot.title = element_text(hjust = 0.5, size = 14)) + 
  scale_x_continuous(breaks = c(0:5)*5+1991)

grid.arrange(p7, p8, ncol=2)


tag_data <- read.csv('./mydata/tag data.csv', na.strings = "NA")

g1 <- ggplot(data = tag_data, aes(x = Year, y = Noun, group = 1)) + 
  geom_line(color = brewer.pal(4, set_col)[1], size = 1.2) + 
  geom_smooth(method="lm", color="red", linetype=2) + 
  geom_point(size=3, shape=18, color = brewer.pal(4, set_col)[1]) + theme_economist() +
  labs(title="Panel A: Trend of Noun Proportion", x="Year", y="Noun Proportion") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14),
        plot.title = element_text(hjust = 0.5, size = 14)) + 
  scale_x_continuous(breaks = c(0:5)*5+1991)

g2 <- ggplot(data = tag_data, aes(x = Year, y = Verb, group = 1)) + 
  geom_line(color = brewer.pal(4, set_col)[2], size = 1.2) + 
  geom_smooth(method="lm", color="red", linetype=2) + 
  geom_point(size=3, shape=19, color = brewer.pal(4, set_col)[2]) + theme_economist() +
  labs(title="Panel B: Trend of Verb Proportion", x="Year", y="Verb Proportion") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14),
        plot.title = element_text(hjust = 0.5, size = 14)) + 
  scale_x_continuous(breaks = c(0:5)*5+1991)

g3 <- ggplot(data = tag_data, aes(x = Year, y = Adjective, group = 1)) + 
  geom_line(color = brewer.pal(4, set_col)[3], size = 1.2) + 
  geom_smooth(method="lm", color="red", linetype=2) + 
  geom_point(size=3, shape=18, color = brewer.pal(4, set_col)[3]) + theme_economist() +
  labs(title="Panel C: Trend of Adjective Proportion", x="Year", y="Adjective Proportion") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14),
        plot.title = element_text(hjust = 0.5, size = 14)) + 
  scale_x_continuous(breaks = c(0:5)*5+1991)

g4 <- ggplot(data = tag_data, aes(x = Year, y = Adverb, group = 1)) + 
  geom_line(color = brewer.pal(4, set_col)[4], size = 1.2) + 
  geom_smooth(method="lm", color="red", linetype=2) + 
  geom_point(size=3, shape=19, color = brewer.pal(4, set_col)[4]) + theme_economist() +
  labs(title="Panel D: Trend of Adverb Proportion", x="Year", y="Adverb Proportion") +  
  theme(axis.title.x=element_text(size=14), 
        axis.title.y=element_text(size=14),
        plot.title = element_text(hjust = 0.5, size = 14)) + 
  scale_x_continuous(breaks = c(0:5)*5+1991)

grid.arrange(g1, g2, g3, g4, ncol=2)






