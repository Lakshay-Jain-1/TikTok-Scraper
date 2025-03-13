from modules.scrapper import extractVideoUrls

"""
Documentation 

Function
extractVideoUrls -> return a list of video url's eg ['https://www.tiktok.com/@pich.solikah/video/7481208166252891412']
    has two parmeters
    first parameter
    searchQueries -> it should be a list of string eg ["Trump"]
    second parameter
    hashtags -> it should be a list of string eg ["fyp"]


"""



def main():
    # phase 1 to extract the url's
    videoUrls =  extractVideoUrls() 
    print(videoUrls) # it will return video url's

    # phase 2


if __name__ == "__main__":
    main()