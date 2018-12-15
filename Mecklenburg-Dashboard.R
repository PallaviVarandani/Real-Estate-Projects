##Mecklenburg County####
###Below code Cleans and Analysis the data to visualize it into the RShiny Dashboard####
##This is just the demonstration with 5 Insights, we can analysis more parameter 
###and also create a dynamic dashboard where user can input the property information to get the insights and trends in a particular county###
### By Pallavi Varandani

# 1. Library
library(shiny)
library(shinythemes)
library(dplyr)
library(readr)
library(RMySQL)
library(data.table)
library(stringi)
library(ggplot2)
require(scales)

# 2. Read data from db
mydb <-  dbConnect(MySQL(), user = 'root', password = 'Vansh@1234',
                   dbname = 'Landis', host = 'localhost', port = 3306)
df <- dbReadTable(mydb,"Mecklenburg")

#3. Cleaning and Transforming the dataset
cols <- names(df)
df[df == "''"] <- NA # replacing blanks with NA
df[df == "'-'"] <- NA # replacing "-" with NA
setDT(df)[, (cols) := lapply(.SD, function(x) type.convert(stri_sub(x, 2, -2)))] #Removing the extra Quotes

#Changing the datatype as per requirements####
df$ParcelID = as.factor(df$ParcelID)
df$AccountNo = as.factor(df$AccountNo)
df$LastSaleDate = as.Date.character(df$LastSaleDate)
df$LastSalePrice = substring(df$LastSalePrice,2)
df$LastSalePrice = as.numeric(gsub(",","",df$LastSalePrice))
df$LandValue = substring(df$LandValue,2)
df$LandValue = as.numeric(gsub(",","",df$LandValue))
df$BuildingValue = substring(df$BuildingValue,2)
df$BuildingValue = as.numeric(gsub(",","",df$BuildingValue))
df$Features = substring(df$Features,2)
df$Features = as.numeric(gsub(",","",df$Features))
df$TotalAppraisedValue = substring(df$TotalAppraisedValue,2)
df$TotalAppraisedValue = as.numeric(gsub(",","",df$TotalAppraisedValue))
df$HeatedArea = as.numeric(gsub(",","",df$HeatedArea))
df$TotalSqFt = as.numeric(gsub(",","",df$TotalSqFt))
df$Bedrooms = as.factor(df$Bedrooms)
#str(df)

#4. Defining the User interface function of the Rshiny Dashboard
ui <- fluidPage(theme = shinytheme("superhero"),
                
                titlePanel(title=h1("Mecklenburg County", align="center")),
                
                sidebarPanel(
                  selectInput("Type", label = h3("Select the Graph:"), 
                              choices = c("Heat VS LastSalePrice VS Bedroom VS Fuel","Story VS LastSalePrice VS Foundation", 
                                          "BuildingValue VS LastSalePrice","Externalwall VS TotalAppraisedValue VS Heat VS Fuel",
                                          "TotalAppraisedValue VS LastSalePrice")),
                  actionButton(inputId = "go", label = "RUN")
                ),
                
                mainPanel(
                  uiOutput("type")
                )
)

#5. defining the backend server function of the R Shiny Dashboard

server <- shinyServer(function(input, output){
  
  #Defining the layout for each output
  output$type <- renderUI({
    check1 <- input$Type == "Heat VS LastSalePrice VS Bedroom VS Fuel" 
    check2 <- input$Type == "Story VS LastSalePrice VS Foundation"
    check3 <- input$Type == "BuildingValue VS LastSalePrice"
    check4 <- input$Type == "Externalwall VS TotalAppraisedValue VS Heat VS Fuel"
    check5 <- input$Type == "TotalAppraisedValue VS LastSalePrice"
  if (check1){
      tabsetPanel(tabPanel("Heat VS LastSalePrice VS Bedroom VS Fuel",plotOutput(outputId = "plot1"),textOutput(outputId = 'text1')))
  }
  else if (check2){
      tabsetPanel(tabPanel("Story VS LastSalePrice VS Foundation",plotOutput(outputId = "plot2"),textOutput(outputId = 'text2')))
  }
    else if (check3){
      tabsetPanel(tabPanel("BuildingValue VS LastSalePrice",plotOutput(outputId = "plot3"),textOutput(outputId = 'text3')))
    }
    else if (check4){
      tabsetPanel(tabPanel("Externalwall VS TotalAppraisedValue VS Heat VS Fuel",plotOutput(outputId = "plot4"),textOutput(outputId = 'text4')))
    }
    else if (check5){
      tabsetPanel(tabPanel("TotalAppraisedValue VS LastSalePrice",plotOutput(outputId = "plot5"),textOutput(outputId = 'text5')))
    }
    else{
      print("Not Applicable")
    }
  })
  
  #plot1
  plot1 <- eventReactive(input$go,{
    ###Heat,LastSalePrice,Bedroom,Fuel###
    ggplot(df, aes(x=Heat, y=LastSalePrice, shape=Bedrooms, color=Fuel)) +
      geom_point()
  })
  
  #plot2
  plot2 <- eventReactive(input$go,{
    ###Story,LastSalePrice,Foundation####
    ggplot(df, aes(x=Story, y=LastSalePrice, shape=Foundation, color=Foundation)) +
      geom_point()
  })
  
  #plot3
  plot3 <- eventReactive(input$go,{
    ###BuildingValue,LastSalePrice####
    ggplot(df, aes(x=BuildingValue, y=LastSalePrice))+geom_point()+scale_x_continuous(labels = comma) 
  })
  
  #plot4
  plot4 <- eventReactive(input$go,{
    ####Externalwall, TotalAppraisedValue,Heat,Fuel#####
    ggplot(df, aes(x=ExternalWall,y=TotalAppraisedValue, shape=Heat, color=Fuel))+geom_point()
  })
  
  #plot 5
  plot5 <- eventReactive(input$go,{
    ####TotalAppraisedValue,LastSalePrice####
    ggplot(df, aes(x=TotalAppraisedValue, y=LastSalePrice))+geom_point()+scale_x_continuous(labels = comma) 
  })
  
  #Insight 1
  text1 <- eventReactive(input$go,{
    print("For Mecklenburg County, A 4 Bedroom property with Heat type Forced Air Ducted and Fuel Type Gas has the highest Last Sale Price, however, the Least Last Price is for Baseboard Heat with Electric Fuel 3 Bedroom Property")
  })
  
  #Insight 2
  text2 <- eventReactive(input$go,{
    print("For Mecklenburg County, A Two Story property with Foundation type Crawl Space has the highest Last Sale Price, whereas, the Least Last Sale Price is for a Bi-Level Story Property with Foundation Crawl Space.")
  })
  
  #Insight 3
  text3 <- eventReactive(input$go,{
    print("For Mecklenburg County, There is positive correlation between Last Sale Price and Building Value, i.e. the higher the Building Value, higher is the Last Sale Price")
  })
  
  #Insight 4
  text4 <- eventReactive(input$go,{
    print("For Mecklenburg County, A property with Heat type Forced Air Ducted,Fuel Type Gas and Face Brick External wall has the highest Last Sale Price, however, the Least Last Price is for Forced Air Ducted Heat with Gas Fuel and Interior Plywood External Wall")
  })
  
  #Insight 5
  text5 <-eventReactive(input$go,{
    print("For Mecklenburg County, There is positive correlation between Last Sale Price and Total Appraised Value, i.e. the higher the Total Appraised Value, higher is the Last Sale Price. However, there are exception when Total Appraised Value is low and still the Last Sale Prices are high.")
  })
  
  ##Defining the outpusa to display
  output$plot1 <- renderPlot({plot1()})
  output$plot2 <- renderPlot({plot2()})
  output$plot3 <- renderPlot({plot3()})
  output$plot4 <- renderPlot({plot4()})
  output$plot5 <- renderPlot({plot5()})
  output$text1 <- renderPrint({text1()})
  output$text2 <- renderPrint({text2()})
  output$text3 <- renderPrint({text3()})
  output$text4 <- renderPrint({text4()})
  output$text5 <- renderPrint({text5()})
  
})


##Calling the Rshiny Dashboard function
shinyApp(ui = ui , server = server)