library(ggplot2)

df <- read.csv(file="sam_statistics.csv",sep="\t",head=T)

ggplot(subset(df,df$alignment != "SRR5629778.ecoli.st131_magicblast.sam"),aes(length,score)) +
  geom_point() +
  stat_smooth(method="glm") +
  facet_grid(alignment ~ .) + 
  geom_hline(yintercept = 30,color="red") +
  geom_hline(yintercept = 50,color="red") +
  theme_minimal()


gm <- glm(score ~ length, data=subset(df,as.character(df$alignment) == "SRR2848544_magicblast_default.sam"))
summary(gm)
2.584e+01


ggplot(df,aes(df$score)) + 
  geom_histogram(binwidth=10) +
  facet_grid(alignment ~ .) +
  theme_minimal()
