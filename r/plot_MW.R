library(readr)
library(ggplot2)
ppmw <- read_csv("~/Desktop/SUI/python/pre_post_mannwhitney.csv")
p <- ggplot(ppmw, aes(Surveys, p)) + geom_bar(stat = "identity", 
    fill = "darkblue") + scale_x_discrete("surveys")+ scale_y_continuous("p value")+ 
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, size=5)) + 
  labs(title = "Bar Chart") + facet_wrap( ~ ppmw$PrePost) 
#+ geom_hline(aes(yintercept=0.05))
