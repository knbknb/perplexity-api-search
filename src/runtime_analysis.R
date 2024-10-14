# Load required libraries
library(tidyverse)
library(jsonlite)

# Load the JSON file
data <- fromJSON("wb33-newman-all-perplexity-queries.json")

convert_to_kb <- function(data_received) {
  if (str_detect(data_received, "KB")) {
    return(as.numeric(str_replace(data_received, "KB", "")))
  } else if (str_detect(data_received, "B")) {
    return(as.numeric(str_replace(data_received, "B", "")) / 1024)  # Convert bytes to kilobytes
  }
  return(NA)  # Handle unexpected cases
}


# Function to split the Model column at the second "-" into 'model_name' and 'variant'
split_model_variant <- function(model) {
    parts <- str_split(model, "-", n = 3)[[1]]  # Split into 3 parts at most
    model_name <- paste(parts[1], parts[2], sep = "-")  # Combine the first two parts as 'model_name'
    variant <- parts[3]  # The third part is 'variant'
    return(c(model_name, variant))
}


# Convert the relevant columns to numeric (removing the units "s" and "KB" if necessary)
data_clean <- data %>%
  mutate(`Total Run Duration` = as.numeric(str_replace(`Total Run Duration`, "s", "")),
         `Average Response Time` = as.numeric(str_replace(`Average Response Time`, "s", "")),
         `Total Data Received (KB)` = as.vector(sapply(`Total Data Received`, convert_to_kb)),
         model_split = map(`Model`, split_model_variant),
         model_name = map_chr(model_split, 1),  # First part of the split
         variant = map_chr(model_split, 2),
         # Split model_name by "-" and keep only the first part as model_family
         model_family = map_chr(str_split(model_name, "-"), 1)
         ) %>%
  select(-model_split, -`Total Data Received`) %>%
    mutate(model_family = case_when( str_detect(model_family, "codellama") ~ "llama",
                                     str_detect(model_family, "mixtral") ~ "mistral",
                                     str_detect(model_family, "sonar") ~ "sonar (llama ft)",
                                     TRUE ~ model_family))


# Plot "Total Run Duration" vs "Average Response Time", colored by "Model"
ggplot(data_clean, aes(x = model_name, y = `Total Run Duration`, fill = model_family)) +
  geom_boxplot() +
  labs(title = "Model vs Average Response Time",
       x = "Model",
       y = "Average Response Time (s)") +
  theme_minimal()
