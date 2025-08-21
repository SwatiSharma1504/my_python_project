import datetime
import webbrowser
import wikipedia
import pyjokes
import os
import requests
import openai
def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        print("Good morning!")
    elif 12 <= hour < 18:
        print("Good afternoon!")
    else:
        print("Good evening!")
    print("I am Jarvis, your AI assistant. How can I help you?")
def take_command():
    return input("\nYou: ").lower()
def get_weather(city_name):
    api_key = "3c9664b522535d3c7c6f3e4a4aad83bf"
    base = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    res = requests.get(base)
    data = res.json()
    if data["cod"] != "404":
        weather = data["main"]
        temp = weather["temp"]
        desc = data["weather"][0]["description"]
        print(f"The temperature in {city_name} is {temp}°C with {desc}.")
    else:
        print("City not found.")
def ai_fallback(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[{"role": "user", "content": query}]
        )
        answer = response.choices[0].message.content.strip()
        print("Jarvis:", answer)
    except Exception as e:
        print("Jarvis: Sorry, I couldn't get an answer from AI.")
        print("Error:", e)
def jarvis():
    wish_user()
    todo_list = []
    while True:
        query = take_command()
        if 'wikipedia' in query:
            try:
                print("Searching Wikipedia...")
                topic = query.replace("wikipedia", "").strip()
                if not topic:
                    topic = input("Please enter the topic you want to search on Wikipedia: ")
                result = wikipedia.summary(topic, sentences=2)
                print("Wikipedia says:", result)
            except wikipedia.exceptions.DisambiguationError as e:
                print("Your query is too broad. Suggestions:")
                print(", ".join(e.options[:5]))
            except wikipedia.exceptions.PageError:
                print("Page not found on Wikipedia.")
            except Exception as e:
                print("Error:", e)
        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://google.com")
        elif 'open chrome' in query:
            try:
                chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(chrome_path)
                print("Chrome opened.")
            except:
                print("Couldn't open Chrome. Check the path or install Chrome first.")
        elif 'search' in query:
            search = input("What should I search for? ")
            webbrowser.open(f"https://www.google.com/search?q={search}")
        elif 'weather' in query:
            city = input("Enter city name: ")
            get_weather(city)
        elif 'time' in query:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Current time: {now}")
        elif 'date' in query:
            today = datetime.date.today()
            print(f"Today's date: {today.strftime('%B %d, %Y')}")
        elif 'remember' in query:
            memory = input("What should I remember? ")
            with open("memory.txt", "w") as f:
                f.write(memory)
            print("I have remembered that.")
        elif 'do you remember' in query:
            try:
                with open("memory.txt", "r") as f:
                    memory = f.read()
                    print(f"You asked me to remember: {memory}")
            except:
                print("I don't remember anything yet.")
        elif 'joke' in query:
            print("😂", pyjokes.get_joke())
        elif 'add to do' in query or 'add task' in query:
            task = input("What task should I add? ")
            todo_list.append(task)
            print("Task added to your to-do list.")
        elif 'show to do' in query or 'show tasks' in query:
            if todo_list:
                print("Your To-Do List:")
                for i, task in enumerate(todo_list, 1):
                    print(f"{i}. {task}")
            else:
                print("You have no tasks yet.")
        elif 'remove to do' in query or 'remove task' in query:
            if todo_list:
                print("Your To-Do List:")
                for i, task in enumerate(todo_list, 1):
                    print(f"{i}. {task}")
                try:
                    index = int(input("Enter task number to remove: "))
                    if 1 <= index <= len(todo_list):
                        removed = todo_list.pop(index - 1)
                        print(f"Removed task: {removed}")
                    else:
                        print("Invalid task number.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("You have no tasks to remove.")
        elif 'open powerpoint' in query:
            try:
                os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE")
                print("PowerPoint opened.")
            except:
                print("Couldn't open PowerPoint. Check the path.")
        elif 'open word' in query:
            try:
                os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
                print("Microsoft Word opened.")
            except:
                print("Couldn't open Word. Check the path.")
        elif 'open excel' in query:
            try:
                os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
                print("Excel opened.")
            except:
                print("Couldn't open Excel. Check the path.")
        elif 'open settings' in query:
            try:
                os.system("start ms-settings:")
                print("Opening Windows Settings...")
            except:
                print("Couldn't open Settings.")
        elif 'open camera' in query:
            try:
                os.system("start microsoft.windows.camera:")
                print("Opening Camera...")
            except:
                print("Couldn't open Camera.")
        elif 'open calculator' in query:
            try:
                os.system("start calc")
                print("Opening Calculator...")
            except:
                print("Couldn't open Calculator.")
        elif 'open file explorer' in query:
            try:
                os.system("explorer")
                print("Opening File Explorer...")
            except:
                print("Couldn't open File Explorer.")
        elif 'exit' in query or 'bye' in query:
            print("Goodbye! Have a productive day.")
            break
        else:
            ai_fallback(query)
if __name__ == "__main__":
    jarvis()