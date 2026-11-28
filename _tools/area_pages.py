#!/usr/bin/env python3
"""Builds the West Delhi implant area pages: /dental-implants-<area>/ and /dental-implants-west-delhi/.

Run from the repository root:  python3 _tools/area_pages.py
The page shell (head styles, header, footer, WhatsApp button, Ads tag) is copied from
same-day-dental-implants-delhi/index.html, so the area pages always match the rest of the site.

Rules for these pages (Dr, Nov 2026): no prices, no free offers, call or message as the next step,
white theme, plain human wording. The clinic is only in Rajouri Garden: every page says so plainly.
Drive times were read from Google Maps on Saturday 28 Nov 2026, early afternoon.
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://dentalimplantsdelhi.com"
HUB = "https://www.sobtidentalcare.com"
UPDATED = "2026-11-28"
CALL = "tel:+918744985976"

e = html.escape


def wa(text):
    return "https://wa.me/918076777307?text=" + quote(text, safe="")


# Each area: what is genuinely different about coming from there. Keep every page distinct.
AREAS = [
    {
        "slug": "janakpuri",
        "name": "Janakpuri",
        "colonies": ["A, B, C and D blocks", "Janakpuri District Centre", "Asalatpur", "Possangipur", "Virender Nagar", "Dabri"],
        "road": "about 5.4 km",
        "drive": "about 19 minutes",
        "route_name": "Najafgarh Road (Shivaji Marg)",
        "from": "Janakpuri District Centre",
        "metro": "Blue Line, 4 stops from Janakpuri East or 5 from Janakpuri West, no change",
        "lede": "Janakpuri is a straight run down Najafgarh Road to our clinic in Rajouri Garden: about 5 km, under 20 minutes by car, or four stops on the Blue Line. If you have been told you need an implant, or your dentures have stopped holding, this page explains what the trip and the treatment look like from Janakpuri.",
        "routes": [
            ("By car", "From Janakpuri District Centre, join Najafgarh Road and drive east past Tilak Nagar and Subhash Nagar into Rajouri Garden. Google Maps shows about 5.4 km and 19 minutes in Saturday afternoon traffic. Weekday evenings take longer near Tilak Nagar market."),
            ("By metro", "From Janakpuri East take the Blue Line towards Noida or Vaishali; Rajouri Garden is four stops on (Tilak Nagar, Subhash Nagar, Tagore Garden, Rajouri Garden). From Janakpuri West, which is also on the Magenta Line, it is five. The clinic is a short walk from Rajouri Garden station, above Rajmandir."),
        ],
        "plan_title": "Fitting implant visits around a Janakpuri day",
        "plan": [
            "Because the trip is short, most Janakpuri patients come in for the consultation and the CBCT scan in one visit, go home with a written plan, and decide in their own time.",
            "Implant surgery is usually booked for a morning. You can be home in Janakpuri for lunch, with soft food for the rest of the day.",
            "If you work in Janakpuri District Centre or along Najafgarh Road, short check-ups can be fitted into a lunch break. Tell the desk when you call.",
        ],
        "faq": [
            ("Is there a Dr Sobti's implant clinic in Janakpuri?", "No. There is one clinic, in Rajouri Garden at J 12/26, First Floor, above Rajmandir. It is about 5 km from Janakpuri District Centre along Najafgarh Road, or four metro stops from Janakpuri East."),
            ("Why come from Janakpuri to Rajouri Garden for an implant?", "Because the scan, the planning, the surgery and the lab that makes your new teeth are in one place. Dr Pushkar Sobti has placed more than 5,000 implants since 2009, and each case is planned on the clinic's own CBCT scanner and placed through a printed guide."),
            ("My parents in Janakpuri have loose dentures. Can implants help?", "Often, yes. Two to four implants can hold a lower denture firmly, or a full jaw can be replaced with fixed teeth on four to six implants. The CBCT scan shows which option the bone allows. See <a href=\"/full-mouth-dental-implants-delhi/\">full mouth implants</a>."),
            ("Can I get an appointment on a Sunday?", "Yes. The clinic is open every day from 10 am to 7 pm, Sundays included. Dr Pushkar Sobti sees implant patients by appointment, so call or WhatsApp first."),
        ],
        "hub": "dentist-janakpuri.html",
    },
    {
        "slug": "vikaspuri",
        "name": "Vikaspuri",
        "colonies": ["Vikaspuri blocks A to L", "Krishna Park", "Hastsal", "Budhela", "Keshopur", "Vikas Nagar"],
        "road": "about 6 km",
        "drive": "about 17 minutes",
        "route_name": "Outer Ring Road and Najafgarh Road",
        "from": "Vikaspuri",
        "metro": "No station inside Vikaspuri; Blue Line from Janakpuri West or Janakpuri East",
        "lede": "Vikaspuri has no metro station of its own, so most people come to us by car: about 6 km and around 17 minutes to the clinic in Rajouri Garden. This page covers the route, the number of trips an implant needs, and the questions Vikaspuri families ask most.",
        "routes": [
            ("By car or cab", "Come out to Outer Ring Road, turn onto Najafgarh Road (Shivaji Marg) and head east past Janakpuri and Tilak Nagar into Rajouri Garden. It is about 6 km and around 17 minutes outside rush hour. There is parking close to the clinic, and a lift to the first floor."),
            ("By metro", "Take an auto or e-rickshaw to Janakpuri West or Janakpuri East and ride the Blue Line towards Noida or Vaishali to Rajouri Garden, five or four stops. The clinic is a short walk from the station."),
        ],
        "plan_title": "Keeping the trips from Vikaspuri low",
        "plan": [
            "Most single implants need three main visits: the consultation with the CBCT scan, the surgery, and the visit for the final tooth after healing. Short check-ups in between take 15 to 20 minutes.",
            "Because Vikaspuri is a car trip for most people, it helps to bring someone along on surgery day, even though you will be awake and able to walk out normally.",
            "If you are coming from Hastsal or Budhela, which are further out, ask for the first appointment of the day to miss the Najafgarh Road traffic.",
        ],
        "faq": [
            ("Do you have a clinic in Vikaspuri?", "No. Our only clinic is in Rajouri Garden, about 6 km from Vikaspuri by road. We would rather tell you that plainly than run a page that pretends otherwise."),
            ("How many times will I have to come from Vikaspuri?", "For a single implant, usually three main visits plus short check-ups. For full mouth implants, fixed temporary teeth go in within about 3 days of surgery, and the final teeth follow after healing. Your written plan lists every visit."),
            ("Is implant surgery painful?", "The area is numbed, so you feel pressure but not pain during surgery, and most people need only ordinary painkillers for a day or two. Read <a href=\"/is-dental-implant-surgery-painful/\">what implant surgery feels like</a>."),
            ("Can an older parent manage the visit?", "Yes. The clinic is on the first floor with a lift, parking is close by, and visits are planned so that nobody waits long."),
        ],
        "hub": "dentist-vikaspuri.html",
    },
    {
        "slug": "paschim-vihar",
        "name": "Paschim Vihar",
        "colonies": ["Paschim Vihar A to D blocks", "Meera Bagh", "Mianwali Nagar", "Jwalaheri", "Sunder Vihar", "Paschim Puri"],
        "road": "about 5 km",
        "drive": "about 24 minutes",
        "route_name": "Rohtak Road and Baba Ramdev Marg",
        "from": "Paschim Vihar East metro",
        "metro": "Green Line to Punjabi Bagh, then Pink Line 2 stops",
        "lede": "From Paschim Vihar the clinic in Rajouri Garden is about 5 km by road, through Punjabi Bagh, or a metro ride with one change. If you are weighing up an implant, a bridge or full mouth teeth, here is how the trip and the treatment work from Paschim Vihar and Meera Bagh.",
        "routes": [
            ("By car", "From Paschim Vihar East, Google Maps takes you along Rohtak Road and Baba Ramdev Marg through Punjabi Bagh to Rajouri Garden: about 5 km and 24 minutes on a Saturday afternoon. From Meera Bagh, Outer Ring Road is often quicker."),
            ("By metro", "Take the Green Line from Paschim Vihar East or West to Punjabi Bagh, walk across to Punjabi Bagh West on the Pink Line, and ride two stops (ESI Basaidarapur, Rajouri Garden). The clinic is a short walk from the station."),
        ],
        "plan_title": "Planning implant visits from Paschim Vihar and Meera Bagh",
        "plan": [
            "Rohtak Road is slow in the evening, so morning and early afternoon slots work best for the longer visits: the scan and consultation, and the surgery.",
            "Many people from Paschim Vihar ask about replacing several teeth at once. A CBCT scan at the first visit shows whether a bridge on two or three implants or a full arch is the better plan, and you get both options in writing.",
            "If an extraction is due, an implant can often go in at the same sitting, which saves a separate trip. See <a href=\"/same-day-dental-implants-delhi/\">same-day implants</a>.",
        ],
        "faq": [
            ("Is there a Dr Sobti's clinic in Paschim Vihar?", "No. The clinic is in Rajouri Garden, about 5 km away through Punjabi Bagh, or a short metro ride with one change at Punjabi Bagh."),
            ("Can I replace a few missing teeth without one implant per tooth?", "Usually, yes. Two implants can carry a three-tooth bridge, and four to six implants can carry a whole jaw of fixed teeth. The scan decides how many you need. See <a href=\"/implant-prosthesis-delhi/\">implant crowns and bridges</a>."),
            ("Is the clinic easy to reach from Meera Bagh?", "Yes. Meera Bagh is about 3.5 km from the clinic in a straight line. Most people come by car along Outer Ring Road or by the Pink Line from Punjabi Bagh West."),
            ("What should I bring to the first visit?", "Any old X-rays or scans, a list of your medicines (especially blood thinners or diabetes tablets), and your questions. The clinic takes its own CBCT scan if one is needed."),
        ],
        "hub": "dentist-paschim-vihar.html",
    },
    {
        "slug": "tilak-nagar",
        "name": "Tilak Nagar",
        "colonies": ["Tilak Nagar", "Chaukhandi", "Fateh Nagar", "Tilak Vihar", "Ashok Nagar", "Krishna Puri"],
        "road": "about 3.2 km",
        "drive": "about 12 minutes",
        "route_name": "Najafgarh Road (Shivaji Marg)",
        "from": "Tilak Nagar metro",
        "metro": "Blue Line, 3 stops, no change",
        "lede": "Tilak Nagar is three metro stops from our clinic in Rajouri Garden, or about 12 minutes by car down Najafgarh Road. That is close enough that an implant does not have to be a big expedition. Here is what to expect.",
        "routes": [
            ("By metro", "From Tilak Nagar take the Blue Line towards Noida or Vaishali. Rajouri Garden is three stops away (Subhash Nagar, Tagore Garden, Rajouri Garden). The clinic is a short walk from the station, above Rajmandir."),
            ("By car or auto", "Najafgarh Road takes you straight from Tilak Nagar to Rajouri Garden: about 3.2 km and 12 minutes on a Saturday afternoon, by Google Maps. Avoid the market stretch in the evening if you can."),
        ],
        "plan_title": "Why the short trip from Tilak Nagar helps",
        "plan": [
            "Living this close means healing check-ups are easy. If anything feels wrong after surgery, you can be in the chair the same day.",
            "Patients from Tilak Nagar often come in first for a broken or painful back tooth. If it cannot be saved, the CBCT scan taken that day shows whether an implant can go in at the time of extraction.",
            "Short visits, such as stitch removal or a check of the healing implant, fit easily into an hour away from the shop or office.",
        ],
        "faq": [
            ("Is there a Dr Sobti's clinic in Tilak Nagar?", "No. The clinic is in Rajouri Garden, three stops from Tilak Nagar on the Blue Line."),
            ("My tooth is broken. Should I save it or get an implant?", "Save it if it can be saved well. A root canal and crown keeps your own tooth. If the root is cracked or there is too little tooth left, an implant is the long-term fix. Dr Pushkar Sobti will tell you which, after an examination and an X-ray or scan."),
            ("How long does an implant take from start to finish?", "Usually 3 to 4 months from surgery to the final tooth, while the implant fuses with the bone. In suitable cases a fixed temporary tooth goes on the same day, so you never walk around with a gap."),
            ("Which implant brands do you use?", "Titanium implants from Osstem, Hiossen and Nobel Biocare. Your written plan names the implant chosen for you and why."),
        ],
        "hub": "dentist-tilak-nagar.html",
    },
    {
        "slug": "moti-nagar",
        "name": "Moti Nagar and Kirti Nagar",
        "short": "Moti Nagar",
        "colonies": ["Moti Nagar", "DLF Capital Greens", "Karampura", "Ramesh Nagar", "Kirti Nagar", "Sudarshan Park", "Basai Darapur"],
        "road": "about 3.6 km",
        "drive": "about 16 minutes",
        "route_name": "Najafgarh Road (Shivaji Marg)",
        "from": "Moti Nagar metro",
        "metro": "Blue Line, 2 stops from Moti Nagar, 3 from Kirti Nagar",
        "lede": "Moti Nagar is two stops from our Rajouri Garden clinic on the Blue Line, and Kirti Nagar is three. If you live in DLF Capital Greens, Karampura, Ramesh Nagar or Kirti Nagar and need one tooth or many replaced, this page explains the trip and the treatment.",
        "routes": [
            ("By metro", "From Moti Nagar take the Blue Line towards Dwarka; Rajouri Garden is two stops (Ramesh Nagar, then Rajouri Garden). From Kirti Nagar it is three. The clinic is a short walk from the station."),
            ("By car", "Drive west along Najafgarh Road (Shivaji Marg) to Rajouri Garden: about 3.6 km and 16 minutes from Moti Nagar on a Saturday afternoon, by Google Maps. DLF Capital Greens is about 4 km away."),
        ],
        "plan_title": "From a Moti Nagar flat to a fixed tooth",
        "plan": [
            "For people living in the DLF Capital Greens towers or in Karampura, the Blue Line is usually faster than the car at office hours. Two stops, then a short walk.",
            "The first visit is a consultation with a CBCT scan. You leave with a written plan that names the implant, the number of visits and the full cost, so there are no surprises later.",
            "If you travel for work, tell us your dates. Surgery and the final tooth can be planned around them.",
        ],
        "faq": [
            ("Do you have a clinic in Moti Nagar or Kirti Nagar?", "No. The clinic is in Rajouri Garden, two or three stops away on the Blue Line, or about 16 minutes by car."),
            ("Is an implant better than a bridge?", "An implant does not need the teeth next to the gap to be cut down, and it keeps the bone from shrinking. A bridge is quicker and can suit you if the neighbouring teeth already need crowns. Read <a href=\"/blog/dental-implant-vs-bridge-vs-denture/\">implants, bridges or dentures</a>."),
            ("Do you make the implant crown in-house?", "Yes. Crowns, bridges and full-arch teeth are designed and milled in the clinic's own lab, Titanium Arts Dental Studio, on the same floor as the surgery."),
            ("Can I message before I visit?", "Yes. Message us on WhatsApp at 80767 77307 or call 87449 85976 with your questions, or send an old X-ray if you have one."),
        ],
        "hub": "dentist-kirti-nagar.html",
    },
    {
        "slug": "punjabi-bagh",
        "name": "Punjabi Bagh",
        "colonies": ["East Punjabi Bagh", "West Punjabi Bagh", "Club Road", "Madipur", "Shivaji Park", "Raja Garden"],
        "road": "about 4 km",
        "drive": "about 17 minutes",
        "route_name": "Club Road and Vishal Cinema Road",
        "from": "Club Road, Punjabi Bagh",
        "metro": "Pink Line, 2 stops from Punjabi Bagh West",
        "lede": "From Club Road in Punjabi Bagh our clinic in Rajouri Garden is about 4 km by road, or two stops on the Pink Line. Punjabi Bagh families often come to us about full mouth implants for a parent, or a single implant after losing a back tooth. Here is what the trip and the treatment involve.",
        "routes": [
            ("By car", "From Club Road, Google Maps routes you via Vishal Cinema Road into Rajouri Garden: about 4 km and 17 minutes on a Saturday afternoon. Parking is close to the clinic, and there is a lift."),
            ("By metro", "From Punjabi Bagh West take the Pink Line towards Mayapuri; Rajouri Garden is two stops (ESI Basaidarapur, then Rajouri Garden). If you are on the Green Line, change at Punjabi Bagh."),
        ],
        "plan_title": "Full mouth implants for a parent in Punjabi Bagh",
        "plan": [
            "When a parent's dentures no longer stay in, the first visit is a consultation and CBCT scan. The family can sit in, see the scan and ask questions. We explain fixed teeth on four to six implants and a removable denture clipped onto implants, side by side.",
            "For a full arch, fixed temporary teeth usually go in within 3 days of surgery, so the trip pattern is a surgery day, a short visit or two that week, check-ups during healing, then the final teeth.",
            "Blood pressure, diabetes and blood thinners are checked before surgery, with the family doctor where needed. See <a href=\"/blog/who-can-get-dental-implants/\">who can get dental implants</a>.",
        ],
        "faq": [
            ("Is there a Dr Sobti's clinic in Punjabi Bagh?", "No. The clinic is in Rajouri Garden, two stops from Punjabi Bagh West on the Pink Line, or about 17 minutes by car."),
            ("Is my mother too old for implants?", "Age alone is rarely the problem. General health, bone and how well conditions like diabetes are controlled matter more. Many patients in their seventies have implants. The scan and a short medical history decide it."),
            ("What is All-on-4 or All-on-6?", "A whole jaw of fixed teeth carried on four or six implants, instead of one implant per tooth. Read about <a href=\"/full-mouth-dental-implants-delhi/\">All-on-X full mouth implants</a>."),
            ("Will the family get the plan in writing?", "Yes. After the scan you get a written plan with the number of implants, the visits and the full cost, so the family can discuss it at home."),
        ],
        "hub": "dentist-punjabi-bagh.html",
    },
    {
        "slug": "pitampura",
        "name": "Pitampura",
        "colonies": ["Kohat Enclave", "Saraswati Vihar", "Sainik Vihar", "Lok Vihar", "Sandesh Vihar", "Harsh Vihar", "Shakti Vihar", "Pushpanjali Enclave", "Netaji Subhash Place"],
        "road": "about 10.4 km",
        "drive": "about 34 minutes",
        "route_name": "Ring Road (Mahatma Gandhi Road)",
        "from": "Madhuban Chowk",
        "metro": "Red Line to Netaji Subhash Place, then Pink Line 4 stops",
        "lede": "From Madhuban Chowk in Pitampura, the clinic in Rajouri Garden is about 10 km down Ring Road, around half an hour by car, or a metro ride with one change at Netaji Subhash Place. If you are planning an implant from Pitampura, this page is about making that trip worth it.",
        "routes": [
            ("By car", "Come down Ring Road (Mahatma Gandhi Road) past Netaji Subhash Place and Punjabi Bagh to Rajouri Garden. Google Maps shows about 10.4 km and 34 minutes from Madhuban Chowk on a Saturday afternoon. Allow more on weekday evenings."),
            ("By metro", "From Pitampura or Kohat Enclave take the Red Line to Netaji Subhash Place and change to the Pink Line towards Mayapuri. Rajouri Garden is four stops on (Shakurpur, Punjabi Bagh West, ESI Basaidarapur, Rajouri Garden)."),
        ],
        "plan_title": "Making the Pitampura trip count",
        "plan": [
            "Send your old X-rays or a photo of the area on WhatsApp before the first visit. It helps us tell you whether a CBCT scan is likely to be needed, so you can plan the time.",
            "The consultation and CBCT scan are done in the same visit, and the written plan is given to you before you leave, so you do not need a second trip just to hear the plan.",
            "Surgery takes one visit. Healing check-ups are short, and some can be done over a WhatsApp photo when nothing is wrong.",
        ],
        "faq": [
            ("Is Dr Sobti's Dental Care in Pitampura?", "No. The clinic is in Rajouri Garden, about 10 km from Madhuban Chowk by road, or four Pink Line stops from Netaji Subhash Place."),
            ("Is it worth travelling from Pitampura for an implant?", "That is your call. What you get is one team for the scan, the planning, the surgery and the lab: Dr Pushkar Sobti has placed more than 5,000 implants since 2009, and the teeth are made on the same floor. That keeps the number of trips low."),
            ("How many trips will I need from Kohat Enclave or Saraswati Vihar?", "Usually three main visits for a single implant (consultation with scan, surgery, final tooth) and two or three short check-ups. Your written plan tells you exactly."),
            ("Do you treat bone loss?", "Yes. Bone grafting, sinus lifts and, for full arches with very little bone, tilted, zygomatic or pterygoid implants. See <a href=\"/bone-grafting-for-dental-implants-delhi/\">bone grafting for implants</a>."),
        ],
        "hub": "dentist-pitampura.html",
    },
    {
        "slug": "rohini",
        "name": "Rohini",
        "colonies": ["Rohini Sectors 3, 7, 8, 9 and 10", "Sectors 11, 13, 15 and 16", "Rohini West", "Rohini East", "Rithala", "Prashant Vihar"],
        "road": "about 12.5 km",
        "drive": "about 35 to 45 minutes",
        "route_name": "Outer Ring Road and Ring Road",
        "from": "Rohini Sector 10, near Rohini West metro",
        "metro": "Red Line to Netaji Subhash Place, then Pink Line 4 stops",
        "lede": "Rohini is a longer trip to our clinic in Rajouri Garden: about 12 km by road, 35 to 45 minutes, or two metro lines. Rohini has many dental clinics of its own, so we will be plain about when the journey makes sense and how we keep it to as few visits as possible.",
        "routes": [
            ("By car", "From Sector 10 near Rohini West, Google Maps takes Outer Ring Road and Ring Road down to Punjabi Bagh and Rajouri Garden: about 12.5 km, 35 to 45 minutes on a Saturday afternoon."),
            ("By metro", "From Rohini West or Rohini East take the Red Line to Netaji Subhash Place (four stops from Rohini West) and change to the Pink Line towards Mayapuri. Rajouri Garden is four stops further. Allow about 45 minutes door to door."),
        ],
        "plan_title": "When the trip from Rohini makes sense",
        "plan": [
            "For a simple single implant, a good implant dentist near you may be the easier choice. The trip makes more sense for full mouth implants, failing teeth that need to come out with implants placed the same day, bone loss, or a second opinion on a plan you have been given.",
            "Send your X-rays, scan or written quote on WhatsApp first. We will tell you honestly whether coming in is worth it.",
            "For full arch treatment we plan the week together: surgery day, fixed temporary teeth within about 3 days, then check-ups spread out during healing.",
        ],
        "faq": [
            ("Do you have a clinic in Rohini?", "No. Our only clinic is in Rajouri Garden, about 12 km from Rohini by road."),
            ("I already have a quote from another clinic. Can you look at it?", "Yes. Message the quote and any scans or X-rays on WhatsApp at 80767 77307. We will tell you what we would do differently, if anything, at your consultation."),
            ("How long will I be at the clinic on surgery day?", "For a single implant, about an hour to an hour and a half including numbing and instructions. For a full arch, plan for most of the day."),
            ("Which implants do you use for full mouth cases?", "Titanium implants from Nobel Biocare, Hiossen and Osstem, chosen for the bone you have. See <a href=\"/full-mouth-dental-implants-delhi/\">All-on-X full mouth implants</a>."),
        ],
        "hub": None,
    },
    {
        "slug": "dwarka",
        "name": "Dwarka",
        "colonies": ["Dwarka Sectors 4 to 7", "Sectors 10 to 14", "Sectors 19 to 23", "Dwarka Mor", "Palam", "Uttam Nagar on the way"],
        "road": "about 12 km",
        "drive": "about 35 to 45 minutes",
        "route_name": "Dabri Dwarka Road (Pankha Road)",
        "from": "Dwarka Sector 10 metro",
        "metro": "Blue Line, direct with no change (15 stops from Sector 10)",
        "lede": "Dwarka is on the same Blue Line as our Rajouri Garden clinic, so you can get here without changing trains. By road it is about 12 km from Sector 10, around 35 to 45 minutes. This page explains when the trip makes sense and how we keep it to as few visits as possible.",
        "routes": [
            ("By metro", "Board the Blue Line at any Dwarka sector station towards Noida or Vaishali and stay on to Rajouri Garden. From Dwarka Sector 10 it is 15 stops, from Dwarka Mor 9, about 35 to 40 minutes. The clinic is a short walk from the station."),
            ("By car", "From Sector 10, Google Maps takes Dabri Dwarka Road (Pankha Road) north to Najafgarh Road and on to Rajouri Garden: about 12 km and 35 to 45 minutes on a Saturday afternoon."),
        ],
        "plan_title": "Planning implants from Dwarka",
        "plan": [
            "Dwarka has plenty of clinics, so the trip usually makes sense for bigger cases: full mouth implants, implants where bone is thin, implants placed straight after an extraction, or a second opinion.",
            "Ask for a late morning slot. The Blue Line is quieter after the office rush, and the consultation, CBCT scan and written plan all happen in that one visit.",
            "On surgery day you will be awake and able to travel home by metro, but for a full arch we suggest someone comes with you and you go home by car.",
        ],
        "faq": [
            ("Is there a Dr Sobti's clinic in Dwarka?", "No. The clinic is in Rajouri Garden, on the Blue Line, with no change of train from any Dwarka sector."),
            ("Why would I travel from Dwarka for implants?", "For one team that does the 3D scan, the planning, the guided surgery and the teeth, under one roof. Dr Pushkar Sobti has placed more than 5,000 implants since 2009 and focuses on full mouth implants."),
            ("Can I send my X-ray before coming?", "Yes. Send it on WhatsApp at 80767 77307 with a line about the problem, and we will tell you what the first visit will involve."),
            ("What if I need a bone graft?", "The CBCT scan shows it before surgery. Many grafts are done in the same sitting as the implant, so it does not always mean an extra trip. See <a href=\"/bone-grafting-for-dental-implants-delhi/\">bone grafting for implants</a>."),
        ],
        "hub": None,
    },
    {
        "slug": "karol-bagh",
        "name": "Karol Bagh and Rajinder Nagar",
        "short": "Karol Bagh",
        "colonies": ["Karol Bagh", "Old Rajinder Nagar", "New Rajinder Nagar", "East Patel Nagar", "West Patel Nagar", "Dev Nagar", "Pusa Road"],
        "road": "about 9 km",
        "drive": "about 35 to 45 minutes",
        "route_name": "Patel Road and Najafgarh Road",
        "from": "Karol Bagh metro",
        "metro": "Blue Line, 7 stops, no change",
        "lede": "Karol Bagh is seven stops from our Rajouri Garden clinic on the Blue Line, with no change of train. By road it is about 9 km along Patel Road and Najafgarh Road. If you live in Karol Bagh, Rajinder Nagar or Patel Nagar, here is how implant treatment with us works from there.",
        "routes": [
            ("By metro", "From Karol Bagh take the Blue Line towards Dwarka. Rajouri Garden is seven stops (Rajendra Place, Patel Nagar, Shadipur, Kirti Nagar, Moti Nagar, Ramesh Nagar, Rajouri Garden), about 15 minutes on the train. The clinic is a short walk from the station."),
            ("By car", "Google Maps offers Patel Road and Najafgarh Road west to Rajouri Garden: about 9 km, 35 to 45 minutes on a Saturday afternoon. Karol Bagh's market traffic is the slow part, so the metro is often quicker."),
        ],
        "plan_title": "Implants from Karol Bagh, Rajinder Nagar and Patel Nagar",
        "plan": [
            "Because the Blue Line is direct, most people from Karol Bagh and Patel Nagar come by metro. The longer visits (consultation with scan, and surgery) are easiest in the late morning.",
            "If you have been quoted for several implants, bring the quote. We will explain whether fewer implants carrying a bridge would do the same job.",
            "Shopkeepers in Karol Bagh often ask for Sunday appointments. The clinic is open on Sunday too, by appointment.",
        ],
        "faq": [
            ("Is there a Dr Sobti's clinic in Karol Bagh?", "No. The clinic is in Rajouri Garden, seven stops from Karol Bagh on the Blue Line."),
            ("Can I come on a Sunday?", "Yes. The clinic is open all seven days, 10 am to 7 pm. Implant visits are by appointment, so call or WhatsApp first."),
            ("Do you replace a front tooth with an implant?", "Yes. Front teeth need careful planning for the gum shape and the look of the crown. In suitable cases a temporary tooth goes on the same day. See <a href=\"/same-day-dental-implants-delhi/\">same-day implants</a>."),
            ("What makes an implant last?", "Good planning, enough bone, a well-fitting crown and regular cleaning. Smoking and uncontrolled diabetes are the commonest reasons implants run into trouble. We explain aftercare before you leave on surgery day."),
        ],
        "hub": "dentist-patel-nagar-rajinder-nagar.html",
    },
]


def shell():
    src = (ROOT / "same-day-dental-implants-delhi" / "index.html").read_text(encoding="utf-8")
    head_end = src.index("<link rel=\"preconnect\"")  # styles, Ads tag, scripts from here to </head>
    styles = src[head_end:src.index("</head>")]
    body_start = src.index("<body>")
    header = src[body_start:src.index("<main class=\"wrap\">")]
    header = header.replace(' aria-current="page"', "")
    footer = src[src.index("</main>") + len("</main>"):]
    return styles, header, footer


STYLES, HEADER, FOOTER = shell()

EXTRA_CSS = """<style id="area-css">
.post .colonies { display: flex; flex-wrap: wrap; gap: .4rem .5rem; list-style: none; margin: 0; padding: 0; }
.post .colonies li { background: var(--surface); border: 1px solid var(--line); border-radius: 999px; padding: .25rem .75rem; font-size: .9rem; }
.post table { width: 100%; border-collapse: collapse; font-size: .95rem; }
.post th, .post td { text-align: left; padding: .6rem .5rem; border-bottom: 1px solid var(--line); vertical-align: top; }
.post td:nth-child(2) { white-space: nowrap; }
.post th { font: 400 .72rem var(--mono); text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }
.post .area-links { columns: 2; padding-left: 1.2rem; margin: 0; }
@media (max-width: 600px) { .post .area-links { columns: 1; } .post table { font-size: .88rem; } }
</style>
"""

PERSON = {"@type": "Person", "@id": f"{SITE}/#drpushkar", "name": "Dr Pushkar Sobti", "jobTitle": "All-on-X Implantologist",
          "honorificSuffix": "BDS, MDS", "image": f"{SITE}/images/dr-pushkar-sobti-portrait.jpg", "url": f"{SITE}/",
          "identifier": {"@type": "PropertyValue", "propertyID": "Dental Council registration", "value": "A-7647"},
          "worksFor": {"@id": f"{SITE}/#clinic"}}


def clinic(area_names):
    return {"@type": "Dentist", "@id": f"{SITE}/#clinic", "name": "Dr Sobti's Dental Care", "url": f"{HUB}/",
            "telephone": "+91-87449-85976",
            "address": {"@type": "PostalAddress", "streetAddress": "J 12/26, First Floor, Rajouri Garden", "addressLocality": "New Delhi",
                        "addressRegion": "Delhi", "postalCode": "110027", "addressCountry": "IN"},
            "geo": {"@type": "GeoCoordinates", "latitude": 28.6407497, "longitude": 77.120662},
            "hasMap": "https://maps.google.com/maps?cid=6577991291147149801", "openingHours": "Mo-Su 10:00-19:00",
            "areaServed": [{"@type": "Place", "name": f"{n}, Delhi"} for n in area_names],
            "sameAs": ["https://maps.google.com/maps?cid=6577991291147149801", f"{HUB}/", "https://www.instagram.com/sobtidentalcare/",
                       "https://www.facebook.com/sobtidentalcare", "https://www.youtube.com/@DrSobtiDental"]}


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def head(title, desc, url, graph):
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/clinic-implant-surgery-room.jpg">
<link rel="icon" href="/images/favicon.png">
<script type="application/ld+json">{ld}</script>
{STYLES}{EXTRA_CSS}</head>
"""


def other_areas(skip):
    items = "".join(f'<li><a href="/dental-implants-{a["slug"]}/">{e(a["name"])}</a></li>' for a in AREAS if a["slug"] != skip)
    return f'<ul class="area-links">{items}<li><a href="/dental-implants-west-delhi/">All areas</a></li></ul>'


def area_page(a):
    url = f"{SITE}/dental-implants-{a['slug']}/"
    short = a.get("short", a["name"])
    title = f"Dental Implants near {a['name']}: Rajouri Garden Clinic | Dr Pushkar Sobti"
    desc = (f"Dental implants for patients from {a['name']}, at Dr Sobti's Dental Care, Rajouri Garden: {a['road']} by road "
            f"({a['drive']} by car), {a['metro']}. CBCT-planned guided implants and full mouth teeth with Dr Pushkar Sobti.")
    msg = wa(f"Hi, I live in {short}. I would like to ask about dental implants.")
    faq_ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(ans)}} for q, ans in a["faq"]]}
    graph = [
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-IN",
         "dateModified": UPDATED, "about": {"@id": f"{SITE}/#clinic"}, "author": {"@id": f"{SITE}/#drpushkar"},
         "reviewedBy": {"@id": f"{SITE}/#drpushkar"}, "lastReviewed": UPDATED,
         "spatialCoverage": {"@type": "Place", "name": f"{a['name']}, Delhi"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Dental implants in West Delhi", "item": f"{SITE}/dental-implants-west-delhi/"},
            {"@type": "ListItem", "position": 3, "name": f"Dental implants near {a['name']}", "item": url}]},
        faq_ld, PERSON, clinic([a["name"]] + [c for c in a["colonies"] if not c[0].isdigit()][:4]),
    ]
    routes = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in a["routes"])
    colonies = "".join(f"<li>{e(c)}</li>" for c in a["colonies"])
    plan = "".join(f"<p>{p}</p>" for p in a["plan"])
    faq = "".join(f"<li><h3>{e(q)}</h3><p>{ans}</p></li>" for q, ans in a["faq"])
    hub = (f' For check-ups, cleaning, root canals, crowns and children\'s dentistry, see <a href="{HUB}/{a["hub"]}">our page for {e(a["name"])} patients</a> on the clinic website.'
           if a["hub"] else f' For other treatments, see the <a href="{HUB}/">clinic website</a>.')
    main = f"""<main class="wrap">
<article class="post">
  <span class="label">West Delhi · {e(a['name'])} · Updated November 2026</span>
  <h1>Dental implants near {e(a['name'])}</h1>
  <div class="byline"><img src="/images/dr-pushkar-sobti-portrait.jpg" alt="Dr Pushkar Sobti" width="800" height="1000"><span><a href="/">Dr Pushkar Sobti</a><br><span class="label">Implantologist, Dr Sobti's Dental Care, Rajouri Garden</span></span></div>

  <p class="lede">{e(a['lede'])}</p>
  <div class="spec">
    <div><b>{e(a['road'].replace('about ', ''))}</b><span class="label">by road from {e(a['from'])}</span></div>
    <div><b>{e(a['drive'].replace('about ', ''))}</b><span class="label">by car, Google Maps</span></div>
    <div><b>5,000+</b><span class="label">implants placed since 2009</span></div>
  </div>
  <p class="cta"><a class="btn" href="{msg}">Message us on WhatsApp</a> <a class="btn alt" href="{CALL}">Call 87449 85976</a></p>

  <h2>Getting to the clinic from {e(short)}</h2>
  <p>There is one clinic: Dr Sobti's Dental Care, J 12/26, First Floor, Rajouri Garden (above Rajmandir), New Delhi 110027, a short walk from Rajouri Garden metro station where the Blue and Pink lines meet. There is no branch in {e(short)}.</p>
  <ul class="rows">{routes}</ul>
  <p class="label">Drive times read from Google Maps on Saturday 28 November 2026, early afternoon. Evenings take longer.</p>

  <h2>Colonies near {e(short)} that use this route</h2>
  <ul class="colonies">{colonies}</ul>

  <h2>{e(a['plan_title'])}</h2>
  {plan}

  <h2>What happens at the clinic</h2>
  <ul class="rows"><li><h3>CBCT scan in the clinic</h3><p>A 3D scan of your jaw is taken on our own MyRay X5 scanner, so you are not sent to an outside centre and back.</p></li><li><h3>Planned on screen, placed through a guide</h3><p>Dr Pushkar Sobti plans each implant on the scan and places it through a 3D-printed guide, which keeps the surgery short and accurate.</p></li><li><h3>Teeth made on the same floor</h3><p>Crowns, bridges and full-arch teeth are milled in our own lab, which saves trips and waiting.</p></li></ul>
  <p>Read more: <a href="/dental-implant-cost-delhi/">what an implant costs and what changes it</a>, <a href="/full-mouth-dental-implants-delhi/">full mouth implants (All-on-X)</a>, <a href="/same-day-dental-implants-delhi/">same-day implants</a> and <a href="/is-dental-implant-surgery-painful/">is implant surgery painful?</a></p>

  <h2>Questions from {e(short)}</h2>
  <ul class="rows faq">{faq}</ul>

  <h2>Other areas</h2>
  <p>Implant patients also come to us from these parts of Delhi.{hub}</p>
  {other_areas(a['slug'])}

  <p class="cta"><a class="btn" href="{msg}">Message us on WhatsApp</a> <a class="btn alt" href="{CALL}">Call the clinic</a></p>
</article>
</main>"""
    return head(title, desc, url, graph) + HEADER + main + FOOTER


def index_page():
    url = f"{SITE}/dental-implants-west-delhi/"
    title = "Dental Implants in West Delhi: Travel Guide by Area | Dr Pushkar Sobti"
    desc = ("Dental implants in West Delhi at Dr Sobti's Dental Care, Rajouri Garden: road distance, drive time and metro route from "
            "Janakpuri, Vikaspuri, Paschim Vihar, Tilak Nagar, Moti Nagar, Punjabi Bagh, Pitampura, Rohini, Dwarka and Karol Bagh.")
    msg = wa("Hi, I would like to ask about dental implants. I live in: ")
    faq = [
        ("Where is the implant clinic?", "At Dr Sobti's Dental Care, J 12/26, First Floor, Rajouri Garden (above Rajmandir), New Delhi 110027, a short walk from Rajouri Garden metro on the Blue and Pink lines. It is the only clinic; there are no branches in the areas listed here."),
        ("Is the clinic open on Sundays?", "Yes, 10 am to 7 pm every day. Dr Pushkar Sobti sees implant patients by appointment, so call 87449 85976 or WhatsApp 80767 77307 first."),
        ("How many visits does an implant need?", "Usually three main visits for a single implant: consultation with a CBCT scan, surgery, and the final tooth after healing, plus short check-ups. Your written plan lists every visit."),
    ]
    graph = [
        {"@type": "CollectionPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-IN",
         "dateModified": UPDATED, "about": {"@id": f"{SITE}/#clinic"}, "author": {"@id": f"{SITE}/#drpushkar"},
         "hasPart": [{"@type": "WebPage", "url": f"{SITE}/dental-implants-{a['slug']}/", "name": f"Dental implants near {a['name']}"} for a in AREAS]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Dental implants in West Delhi", "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in faq]},
        PERSON, clinic(["West Delhi"] + [a["name"] for a in AREAS]),
    ]
    rows = "".join(
        f'<tr><td><a href="/dental-implants-{a["slug"]}/">{e(a["name"])}</a></td><td>{e(a["road"].replace("about ", ""))}</td>'
        f'<td>{e(a["drive"].replace("about ", ""))}</td><td>{e(a["metro"])}</td></tr>' for a in AREAS)
    faq_html = "".join(f"<li><h3>{e(q)}</h3><p>{e(ans)}</p></li>" for q, ans in faq)
    main = f"""<main class="wrap">
<article class="post">
  <span class="label">West Delhi · Updated November 2026</span>
  <h1>Dental implants in West Delhi</h1>
  <div class="byline"><img src="/images/dr-pushkar-sobti-portrait.jpg" alt="Dr Pushkar Sobti" width="800" height="1000"><span><a href="/">Dr Pushkar Sobti</a><br><span class="label">Implantologist, Dr Sobti's Dental Care, Rajouri Garden</span></span></div>
  <p class="lede">Our implant clinic is in Rajouri Garden, where the Blue and Pink metro lines meet, so most of West Delhi is one train or a short drive away. Pick your area for the route, the drive time and the questions people from there ask.</p>
  <p class="cta"><a class="btn" href="{msg}">Message us on WhatsApp</a> <a class="btn alt" href="{CALL}">Call 87449 85976</a></p>

  <h2>Distance and travel time by area</h2>
  <table><thead><tr><th>Area</th><th>By road</th><th>By car</th><th>By metro</th></tr></thead><tbody>{rows}</tbody></table>
  <p class="label">Road distance and drive time from Google Maps, Saturday 28 November 2026, early afternoon.</p>

  <h2>Very close to the clinic</h2>
  <p>Tagore Garden, Subhash Nagar, Ramesh Nagar, Hari Nagar, Mayapuri and Naraina are one or two stops or a few minutes away. For everyday dental care in these colonies, see the <a href="{HUB}/dentist-west-delhi.html">clinic's West Delhi page</a>.</p>

  <h2>Questions</h2>
  <ul class="rows faq">{faq_html}</ul>
  <p class="cta"><a class="btn" href="{msg}">Message us on WhatsApp</a> <a class="btn alt" href="{CALL}">Call the clinic</a></p>
</article>
</main>"""
    return head(title, desc, url, graph) + HEADER + main + FOOTER


def main():
    for a in AREAS:
        out = ROOT / f"dental-implants-{a['slug']}" / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(area_page(a), encoding="utf-8")
    out = ROOT / "dental-implants-west-delhi" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(index_page(), encoding="utf-8")
    print(f"wrote {len(AREAS) + 1} pages")


if __name__ == "__main__":
    main()
