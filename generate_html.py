import socketserver
import http.server
import json
import random

with open('export.json', 'r') as f:
    export = json.load(f)

print(export)

quips = {}

# Total journeys
if export['total_journeys'] < 10:
    options = ["You need to get out more!", "Are you a tourist?",
               "You know you need to tap in, right?"]
elif export['total_journeys'] < 100:
    options = ["You've been out and about!", "You're getting yourself out there!",
               "You're getting the hang of the Tube!"]
elif export['total_journeys'] < 500:
    options = ["We get it, you're a Londoner!",
               "You're a regular!", "You're a Londoner now!"]
else:
    options = ["You need to spend more time above ground!",
               "Do you ever leave London?", "Do you qualify for a gold Oyster card?"]
quips['total_journeys'] = random.choice(options)

# Time spent travelling
if export['average_journey_time'] < 15:
    options = ["Alright, speed demon!", "You don't mess around!"]
elif export['average_journey_time'] < 40:
    options = ["Enough time for a good book.", "Commute life!"]
elif export['average_journey_time'] < 70:
    options = ["Sorry about your commute!", "What time do you call this?"]
else:
    options = ["You really need to move closer...",
               "Do you even live in the M25?"]
quips['average_journey_time'] = random.choice(options)

# Amount of money spent
float_charge = float(export['total_charge'])
if float_charge < 20:
    options = ["Someone doesn't tap in!", "Have you even been on the Tube?"]
elif float_charge < 100:
    options = ["You're getting there!", "You're getting the hang of it!"]
elif float_charge < 500:
    options = ["You're funding TfL better than the government!"]
else:
    options = ["Anything you'd rather spend that on?"]
quips['total_charge'] = random.choice(options)


with open('export.html', 'w+') as w:
    w.write("""<!DOCTYPE html>
<html>
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
    <script src="https://kit.fontawesome.com/afa08cc3f0.js" crossorigin="anonymous"></script>
    <title>My TfL Wrapped</title>

    <style>
        .feature-icon {
            width: 4rem;
            height: 4rem;
            border-radius: .75rem;
        }

        .subtext {
            color: #999;
        }

        .icon-link > .bi {
            margin-top: .125rem;
            margin-left: .125rem;
            fill: currentcolor;
            transition: transform .25s ease-in-out;
        }

        .icon-link:hover > .bi {
            transform: translate(.25rem);
        }

        .icon-square {
            width: 3rem;
            height: 3rem;
            border-radius: .75rem;
        }

        .text-shadow-1 { text-shadow: 0 .125rem .25rem rgba(0, 0, 0, .25); }
        .text-shadow-2 { text-shadow: 0 .25rem .5rem rgba(0, 0, 0, .25); }
        .text-shadow-3 { text-shadow: 0 .5rem 1.5rem rgba(0, 0, 0, .25); }

        .card-cover {
            background-repeat: no-repeat;
            background-position: center center;
            background-size: cover;
        }

        .feature-icon-small {
            width: 3rem;
            height: 3rem;
        }
    </style>

</head>
<body>""")

    w.write(u"""
<div class="container">
    <header class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
      <a href="/" class="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-dark text-decoration-none">
        <span class="fs-4"><i class="fa-solid fa-location-dot"></i> TfL Tracked</span>
      </a>

      <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
        <li><a href="#" class="nav-link px-2 link-secondary"><i class="fa-solid fa-home"></i> Summary</a></li>
        <li><a href="#" class="nav-link px-2 link-dark"><i class="fa-solid fa-bus"></i> Bus</a></li>
        <li><a href="#" class="nav-link px-2 link-dark"><i class="fa-solid fa-train-subway"></i> Trains</a></li>
      </ul>
    </header>
  </div>
""")

    w.write(f"""
<div class="container my-5">
    <div class="row p-4 pb-0 pe-lg-0 pt-lg-5 align-items-center rounded-3 border shadow-lg">
        <div class="col-lg-7 p-3 p-lg-5 pt-lg-3">
            <h1 class="display-4 fw-bold lh-1">Welcome to TfL Tracked!</h1>
            <p class="lead">Here's some personalised statistics from your journeys between <b>{export['date_range']['first']}</b> to <b>{export['date_range']['last']}</b>.</p>
        </div>
    </div>
</div>""")

    w.write(f"""
<div class="container px-4 py-5" id="featured-3">
    <h2 class="pb-2 border-bottom">First, the headlines.</h2>
    <div class="row g-4 py-5 row-cols-1 row-cols-lg-3">
      <div class="feature col">
        <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
          <i class="fa-solid fa-route"></i>
        </div>
        <h3 class="fs-2">{export['total_journeys']} journeys</h3>
        <p>That's around {export['date_range']['journeys_per_day']} journeys per day. {quips['total_journeys']}</p>
      </div>
      <div class="feature col">
        <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
          <i class="fa-solid fa-stopwatch"></i>
        </div>
        <h3 class="fs-2">{export['time_spent_travelling']} minutes</h3>
        <p>That's around {export['average_journey_time']} minutes per journey. {quips['average_journey_time']} <span class="subtext">Excludes bus journeys and journeys where you didn't tap out.</span></p>
      </div>
      <div class="feature col">
        <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
          <i class="fa-solid fa-sterling-sign"></i>
        </div>
        <h3 class="fs-2">£{export['total_charge']} spent</h3>
        <p>That's around £{export['average_charge']} per journey. {quips['total_charge']} <span class="subtext">Includes penalties and journeys where you were capped.</span></p>
      </div>
    </div>
  </div>
    """)

    w.write(f"""
</body>
</html>
    """)

print("Outputted to export.html")

PORT = 8081
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
