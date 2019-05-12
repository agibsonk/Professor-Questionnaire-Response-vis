library(ggplot2)
library(stringr)
library(dplyr)
library(readr)
library(ggrepel)

#Read professor csv file, columns are Professor_Name, Average Score/Rating, Professor Department
teacher_file <- read_csv("teacher_file.csv")
#Converting to a data frame
teacher_file = as.data.frame(teacher_file)

#Merging duplicate professors by averaging the score, preserving department label as well
teacher_file =teacher_file %>% group_by(Professor_Name, Department) %>% mutate_each(list(mean), -(3)) %>% distinct

Departments = teacher_file$Department
Averages = teacher_file$Average_Rating
Professor = teacher_file$Professor_Name

#Plotting using ggrepel to add professor names beside points, keeping seed constant
set.seed(40)
p = ggplot(teacher_file, aes(x = Departments,
                             y = Averages,
                             color = Departments, 
                             label = Professor
                             ))+
  geom_point() +
  ggtitle("Average Questionnaire Response Score") +
  xlab("\nTeaching Department")+
  ylab("Average Response Score Out of 7\n")+
  scale_y_continuous(breaks = seq(0, 7, 1))+
  theme_minimal()+
  theme(legend.position="none")+
  geom_text_repel(size = 2.25, point.padding = 0.1, fontface = 2)
#Plot graph

p + theme(
  plot.title = element_text(face = "bold"),
  axis.title = element_text(face = "bold")
)


