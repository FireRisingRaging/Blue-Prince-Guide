#!/usr/bin/env python3
"""Builds assets/rooms-data.js.

Provenance is tracked per field so the page can show what is verified.
  W = blueprince.wiki.gg (Special Floorplans / Red Rooms / Bedrooms tables)
  T = TFMurphy datamining posts
  ? = not yet sourced, left blank on purpose

Chess badges are hand-maintained here in CHESS and emitted per room as
"chess". Edit that dict and re-run to rebuild assets/rooms-data.js.
"""
import json, io

# ---------------------------------------------------------------- wiki fields
# name: (img, colors, gems, baseRarity)   -- all straight off the wiki tables
W = {
 "The Pool":("ThePool",["Blueprint"],1,"Standard"),
 "Bookshop":("Bookshop",["Shop"],1,"Rare"),
 "Laboratory":("Laboratory",["Blueprint"],1,"Standard"),
 "Commissary":("Commissary",["Shop"],1,"Standard"),
 "Observatory":("Observatory",["Blueprint"],1,"Standard"),
 "Nursery":("Nursery",["Bedroom"],1,"Commonplace"),
 "Servant's Quarters":("ServantsQuarters",["Bedroom"],1,"Unusual"),
 "Aquarium":("Aquarium",["Red Room","Green Room","Hallway","Bedroom","Shop","Blackprint","Blueprint"],1,"Unusual"),
 "Security":("Security",["Blueprint"],1,"Standard"),
 "Kitchen":("Kitchen",["Shop"],1,"Commonplace"),
 "Secret Passage":("SecretPassage",["Hallway"],1,"Unusual"),
 "Treasure Trove":("TreasureTrove",["Blackprint"],1,"Unusual"),
 "Clock Tower":("ClockTower",["Blueprint"],1,"Unusual"),
 "Classroom":("Classroom",["Blueprint"],1,"Unusual"),
 "Walk-In Closet":("WalkinCloset",["Blueprint"],1,"Standard"),
 "Drawing Room":("DrawingRoom",["Blueprint"],1,"Commonplace"),
 "Greenhouse":("Greenhouse",["Green Room"],1,"Standard"),
 "Patio":("Patio",["Green Room"],1,"Standard"),
 "Laundry Room":("LaundryRoom",["Shop"],1,"Rare"),
 "Conservatory":("Conservatory",["Green Room"],1,"Unusual"),
 "Locksmith":("Locksmith",["Shop"],1,"Unusual"),
 "Courtyard":("Courtyard",["Green Room"],1,"Standard"),
 "Rumpus Room":("RumpusRoom",["Blueprint"],1,"Standard"),
 "Solarium":("Solarium",["Green Room"],1,"Standard"),
 "Locker Room":("LockerRoom",["Blueprint"],1,"Rare"),
 "Garage":("Garage",["Blueprint"],1,"Unusual"),
 "Boiler Room":("BoilerRoom",["Blueprint"],1,"Unusual"),
 "Ballroom":("Ballroom",["Blueprint"],2,"Unusual"),
 "Office":("Office",["Blueprint"],2,"Standard"),
 "Drafting Studio":("DraftingStudio",["Blueprint"],2,"Rare"),
 "Foyer":("Foyer",["Hallway"],2,"Unusual"),
 "Master Bedroom":("MasterBedroom",["Bedroom"],2,"Rare"),
 "Passageway":("Passageway",["Hallway"],2,"Commonplace"),
 "Veranda":("Veranda",["Green Room"],2,"Unusual"),
 "Casino":("Casino",["Shop"],2,"Unusual"),
 "Music Room":("MusicRoom",["Blueprint"],2,"Unusual"),
 "Showroom":("Showroom",["Shop"],2,"Rare"),
 "Vestibule":("Vestibule",["Hallway"],2,"Unusual"),
 "Cloister":("Cloister",["Green Room"],3,"Unusual"),
 "Vault":("Vault",["Blueprint"],3,"Rare"),
 "Attic":("Attic",["Blueprint"],3,"Rare"),
 "Rotunda":("Rotunda",["Blueprint"],3,"Rare"),
 "Trophy Room":("TrophyRoom",["Blueprint"],5,"Rare"),
 "Throne Room":("ThroneRoom",["Blackprint"],5,"Rare"),
 # Red Rooms table
 "Lavatory":("Lavatory",["Red Room"],0,"Standard"),
 "Chapel":("Chapel",["Red Room"],0,"Commonplace"),
 "Maid's Chamber":("MaidsChamber",["Red Room","Bedroom"],0,"Unusual"),
 "Archives":("Archives",["Red Room"],0,"Unusual"),
 "Gymnasium":("Gymnasium",["Red Room"],0,"Standard"),
 "Darkroom":("Darkroom",["Red Room"],0,"Standard"),
 "Weight Room":("WeightRoom",["Red Room"],0,"Rare"),
 "Furnace":("Furnace",["Red Room"],0,"Rare"),
 "Lost & Found":("Lost&Found",["Red Room"],0,"Unusual"),
 "Closed Exhibit":("ClosedExhibit",["Red Room"],0,"Rare"),
 # Bedrooms table
 "Bedroom":("Bedroom",["Bedroom"],0,"Commonplace"),
 "Boudoir":("Boudoir",["Bedroom"],0,"Standard"),
 "Guest Bedroom":("GuestBedroom",["Bedroom"],0,"Commonplace"),
 "Bunk Room":("BunkRoom",["Bedroom"],0,"Unusual"),
 "Her Ladyship's Chamber":("HerLadyshipsChamber",["Bedroom"],0,"Rare"),
 "Dormitory":("Dormitory",["Bedroom"],0,"Standard"),
 "Hovel":("Hovel",["Bedroom"],0,"Unusual"),
}

# ------------------------------------------------------ wiki: free floorplans
# Every room absent from the Special Floorplans table costs 0 gems -- that page
# states it lists all gem-costing floorplans except Upgrades, so absence is the
# source, not an assumption.
#   colours : Category:Blueprints / Hallways / Green Rooms / Shops (+ directory pages)
#   rarity  : Category:{Commonplace,Standard,Unusual,Rare} rarity rooms
# name: (colors, baseRarity). None rarity = preplaced, never drafted, no rarity shown.
W0 = {
 # Blueprints
 "The Foundation":(["Blueprint"],"Rare"),
 "Entrance Hall":(["Blueprint"],None),
 "Spare Room":(["Blueprint"],"Commonplace"),
 "Parlor":(["Blueprint"],"Commonplace"),
 "Billiard Room":(["Blueprint"],"Commonplace"),
 "Gallery":(["Blueprint"],"Rare"),
 "Room 8":(["Blueprint"],"Rare"),
 "Closet":(["Blueprint"],"Commonplace"),
 "Storeroom":(["Blueprint"],"Commonplace"),
 "Nook":(["Blueprint"],"Commonplace"),
 "Den":(["Blueprint"],"Commonplace"),
 "Wine Cellar":(["Blueprint"],"Unusual"),
 "Pantry":(["Blueprint"],"Commonplace"),
 "Study":(["Blueprint"],"Unusual"),
 "Library":(["Blueprint"],"Unusual"),
 "Chamber of Mirrors":(["Blueprint"],"Rare"),
 "Utility Closet":(["Blueprint"],"Standard"),
 "Pump Room":(["Blueprint"],"Unusual"),
 "Workshop":(["Blueprint"],"Unusual"),
 "Sauna":(["Blueprint"],"Unusual"),
 "Coat Check":(["Blueprint"],"Standard"),
 "Mail Room":(["Blueprint"],"Unusual"),
 "Freezer":(["Blueprint"],"Rare"),
 "Dining Room":(["Blueprint"],"Standard"),
 "Conference Room":(["Blueprint"],"Unusual"),
 "Antechamber":(["Blueprint"],None),
 "Room 46":(["Blueprint"],None),
 "Dovecote":(["Blueprint"],"Unusual"),
 "The Kennel":(["Blueprint"],"Standard"),
 "Planetarium":(["Blueprint"],"Standard"),
 "Mechanarium":(["Blueprint"],"Unusual"),
 # Hallways
 "Hallway":(["Hallway"],"Commonplace"),
 "West Wing Hall":(["Hallway"],"Standard"),
 "East Wing Hall":(["Hallway"],"Unusual"),
 "Corridor":(["Hallway"],"Commonplace"),
 "Great Hall":(["Hallway"],"Unusual"),
 "Tunnel":(["Hallway"],"Standard"),
 # Green Rooms
 "Terrace":(["Green Room"],"Standard"),
 "Morning Room":(["Green Room"],"Rare"),
 "Secret Garden":(["Green Room"],"Rare"),
 # Shops
 "Armory":(["Shop"],"Standard"),            # wiki page: The Armory
 "Mount Holly Gift Shop":(["Shop"],"Rare"), # wiki page: Gift Shop
}

# ------------------------------------------------- TFMurphy: default dynamic rarity
DR_DEFAULT = {
 "Billiard Room":"Standard","Garage":"Commonplace","Locker Room":"Standard","Vault":"Unusual",
 "Library":"Standard","Drafting Studio":"Unusual","Pump Room":"Standard","Security":"Commonplace",
 "Sauna":"Standard","Freezer":"Unusual","Bunk Room":"Standard","Her Ladyship's Chamber":"Commonplace",
 "Master Bedroom":"Unusual","West Wing Hall":"Commonplace","East Wing Hall":"Standard",
 "Patio":"Commonplace","Courtyard":"Commonplace","Veranda":"Standard","Greenhouse":"Commonplace",
 "Morning Room":"Commonplace","Commissary":"Commonplace","Locksmith":"Standard",
 "Showroom":"Unusual","Mount Holly Gift Shop":"Unusual","Classroom":"Standard",
 "Closed Exhibit":"Unusual","Terrace":"Rare",
}

# TFMurphy: first-week overrides. Empty string = no DR set that day.
WEEK1 = {
 "Workshop":      ["Unusual","","","",""],
 "Commissary":    ["Unusual","Commonplace","Commonplace","Commonplace","Commonplace"],
 "Darkroom":      ["Unusual","","","",""],
 "Billiard Room": ["Unusual","Unusual","Standard","Standard","Standard"],
 "The Pool":      ["Unusual","Unusual","","",""],
 "Drafting Studio":["Rare","Rare","Unusual","Unusual","Unusual"],
 "Pump Room":     ["Rare","Rare","Standard","Standard","Standard"],
 "Coat Check":    ["Rare","Rare","","",""],
 "Freezer":       ["Rare","Rare","Unusual","Unusual","Unusual"],
 "Observatory":   ["Unusual","Unusual","","",""],
 "Lavatory":      ["Commonplace","Commonplace","","",""],
 "Archives":      ["Rare","Rare","","",""],
 "Ballroom":      ["Unusual","Unusual","Unusual","",""],
 "Library":       ["Rare","Rare","Rare","Standard","Standard"],
 "Laboratory":    ["Unusual","Unusual","Unusual","",""],
 "Gymnasium":     ["Unusual","Unusual","Unusual","",""],
 "Study":         ["Rare","Rare","Rare","Rare",""],
 "Master Bedroom":["Rare","Rare","Rare","Rare","Unusual"],
}

# TFMurphy: what V Mode activation sets. "Reset" = drop DR, fall back to base.
VMODE = {
 "Boiler Room":"Standard","Pump Room":"Standard","Workshop":"Standard",
 "Utility Closet":"Commonplace","Commissary":"Commonplace",
 "Billiard Room":"Reset","Ballroom":"Reset","Library":"Reset","Laboratory":"Reset",
 "Coat Check":"Reset","Freezer":"Reset","Dining Room":"Reset","Archives":"Reset",
 "Gymnasium":"Reset","Darkroom":"Reset",
}

# ------------------------------------------- TFMurphy: placement restrictions
# "O" in his tables means allowed. Blank means not allowed.
# wing = (west edge, east edge, W/E pierce); ns = (S/N edge, S/N pierce)
WING = {
 "The Foundation":("","",""),"Spare Room":("O","O",""),"Rotunda":("","",""),
 "Parlor":("O","O","O"),"Billiard Room":("O","O","O"),"Gallery":("O","O",""),
 "Closet":("O","O","O"),"Walk-In Closet":("O","O","O"),"Attic":("O","O","O"),
 "Storeroom":("O","O","O"),"Nook":("O","O","O"),"Garage":("Advance","","West Wing"),
 "Music Room":("O","O","O"),"Locker Room":("O","O",""),"Den":("O","O","O"),
 "Wine Cellar":("O","O","O"),"Trophy Room":("O","O","O"),"Ballroom":("O","O",""),
 "Pantry":("O","O","O"),"Rumpus Room":("O","O",""),"Vault":("O","O","O"),
 "Office":("O","O","O"),"Drawing Room":("O","O","O"),"Study":("O","O","O"),
 "Library":("O","O","O"),"Chamber of Mirrors":("","",""),"The Pool":("O","O","O"),
 "Drafting Studio":("O","O",""),"Utility Closet":("O","O","O"),
 "Boiler Room":("Retreat","Advance",""),"Pump Room":("O","O","O"),"Security":("O","O","O"),
 "Workshop":("O","O",""),"Laboratory":("O","O","O"),"Sauna":("O","O","O"),
 "Coat Check":("O","O","O"),"Mail Room":("O","O","O"),"Freezer":("O","O","O"),
 "Dining Room":("O","O","O"),"Observatory":("O","O","O"),"Conference Room":("O","O","O"),
 "Aquarium":("O","O","O"),"Bedroom":("O","O","O"),"Boudoir":("O","O","O"),
 "Guest Bedroom":("O","O","O"),"Nursery":("O","O","O"),"Servant's Quarters":("O","O","O"),
 "Bunk Room":("O","O","O"),"Her Ladyship's Chamber":("Retreat","",""),
 "Master Bedroom":("","O","East Wing"),"Hallway":("","",""),
 "West Wing Hall":("O","","West Wing"),"East Wing Hall":("","O","East Wing"),
 "Corridor":("O","O",""),"Passageway":("","",""),"Secret Passage":("O","O",""),
 "Foyer":("O","O",""),"Great Hall":("","",""),"Terrace":("","","O"),
 "Patio":("Advance","Retreat","O"),"Courtyard":("O","O","O"),"Cloister":("","",""),
 "Veranda":("O","O",""),"Greenhouse":("Retreat","Advance",""),
 "Morning Room":("Retreat","Advance","O"),"Commissary":("O","O","O"),"Kitchen":("O","O","O"),
 "Locksmith":("O","O","O"),"Showroom":("O","O",""),"Laundry Room":("O","O","O"),
 "Armory":("O","O","O"),"Mount Holly Gift Shop":("O","O","O"),"Lavatory":("O","O","O"),
 "Chapel":("O","O","O"),"Maid's Chamber":("O","O","O"),"Archives":("","",""),
 "Gymnasium":("O","O","O"),"Darkroom":("O","O","O"),"Weight Room":("","",""),
 "Furnace":("O","O","O"),"Dovecote":("","","O"),"The Kennel":("O","O",""),
 "Clock Tower":("Retreat","Retreat","O"),"Classroom":("O","O","O"),
 "Solarium":("Retreat","Retreat","O"),"Dormitory":("O","O","O"),"Vestibule":("","",""),
 "Casino":("O","O","O"),"Planetarium":("O","O","O"),"Mechanarium":("","",""),
 "Treasure Trove":("O","O","O"),"Throne Room":("","","O"),"Lost & Found":("O","O","O"),
 "Conservatory":("","",""),"Tunnel":("O","O",""),"Closed Exhibit":("O","O","O"),
}
NS = {
 "The Foundation":("",""),"Spare Room":("O",""),"Rotunda":("",""),"Parlor":("O","O"),
 "Billiard Room":("O","O"),"Gallery":("O",""),"Closet":("O","O"),"Walk-In Closet":("O","O"),
 "Attic":("O","O"),"Storeroom":("O","O"),"Nook":("O","O"),"Garage":("",""),
 "Music Room":("O","O"),"Locker Room":("O",""),"Den":("O","O"),"Wine Cellar":("O","O"),
 "Trophy Room":("O","O"),"Ballroom":("O",""),"Pantry":("O","O"),"Rumpus Room":("O",""),
 "Vault":("O","O"),"Office":("O","O"),"Drawing Room":("O","O"),"Study":("O","O"),
 "Library":("O","O"),"Chamber of Mirrors":("",""),"The Pool":("O","O"),
 "Drafting Studio":("O",""),"Utility Closet":("O",""),"Boiler Room":("",""),
 "Pump Room":("North Edge","O"),"Security":("O","O"),"Workshop":("O",""),
 "Laboratory":("O","O"),"Sauna":("South Edge","O"),"Coat Check":("O","O"),
 "Mail Room":("O","O"),"Freezer":("O","O"),"Dining Room":("O","O"),"Observatory":("O","O"),
 "Conference Room":("O","O"),"Aquarium":("O","O"),"Bedroom":("O","O"),"Boudoir":("","O"),
 "Guest Bedroom":("O","O"),"Nursery":("O","O"),"Servant's Quarters":("O","O"),
 "Bunk Room":("O","O"),"Her Ladyship's Chamber":("",""),"Master Bedroom":("",""),
 "Hallway":("O","O"),"West Wing Hall":("",""),"East Wing Hall":("",""),
 "Corridor":("O",""),"Passageway":("",""),"Secret Passage":("",""),"Foyer":("O",""),
 "Great Hall":("",""),"Terrace":("",""),"Patio":("",""),"Courtyard":("O","O"),
 "Cloister":("",""),"Veranda":("",""),"Greenhouse":("",""),"Morning Room":("",""),
 "Commissary":("O","O"),"Kitchen":("O","O"),"Locksmith":("O","O"),"Showroom":("O",""),
 "Laundry Room":("O","O"),"Armory":("","O"),"Mount Holly Gift Shop":("South Edge",""),
 "Lavatory":("O","O"),"Chapel":("North Edge","O"),"Maid's Chamber":("North Edge","O"),
 "Archives":("",""),"Gymnasium":("North Edge","O"),"Darkroom":("O","O"),
 "Weight Room":("",""),"Furnace":("O","O"),"Dovecote":("","O"),"The Kennel":("South Edge",""),
 "Clock Tower":("O","O"),"Classroom":("O","O"),"Solarium":("","O"),
 "Dormitory":("North Edge",""),"Vestibule":("",""),"Casino":("O","O"),
 "Planetarium":("South Edge","O"),"Mechanarium":("",""),"Treasure Trove":("O","O"),
 "Throne Room":("",""),"Lost & Found":("North Edge","O"),"Conservatory":("",""),
 "Tunnel":("",""),"Closed Exhibit":("North Edge","O"),
}
NO_CENTER = {"Garage","Her Ladyship's Chamber","Master Bedroom","West Wing Hall","East Wing Hall",
 "Terrace","Patio","Veranda","Greenhouse","Morning Room","Conservatory"}
CORNER_OK = {"Parlor","Billiard Room","Closet","Walk-In Closet","Attic","Storeroom","Nook",
 "Music Room","Wine Cellar","Trophy Room","Pantry","Vault","Office","Study","Library",
 "Utility Closet","Pump Room","Laboratory","Sauna","Coat Check","Mail Room","Freezer",
 "Observatory","Bedroom","Boudoir","Guest Bedroom","Nursery","Servant's Quarters","Bunk Room",
 "Commissary","Kitchen","Locksmith","Laundry Room","Armory","Lavatory","Maid's Chamber",
 "Furnace","Clock Tower","Classroom","Solarium","Dormitory","Casino","Planetarium",
 "Treasure Trove","Lost & Found","Conservatory"}

# TFMurphy: per-room quirks worth surfacing on the card.
NOTES = {
 "Garage":["Weighted Room at 90%, or 92.5% once the West Gate is unlocked. That 92.5% is a bug: the script rolls 25% first, then falls through to the 90%.",
   "Needs Day 3+ or V Mode. Slots 1 and 2 must not both be Dead Ends. One attempt per day.",
   "Intended for West Advance or West Pierce into Rank 4 to 8. Removed from the list at Rank 2 or 3, added back at Rank 4+.",
   "Shares a sublist with East Pierce, so it is always stripped from East Pierce before drafting.",
   "Cannot be rotated. Enters from South or East; the room reshapes to stay against the west wall.",
   "Rarity cannot be changed in the Conservatory.",
   "Powered Room for duct draws."],
 "Utility Closet":["Weighted Room at 20%. Needs Day 2+, the West Gate still locked, and the Garage already drafted today.",
   "Slots 1 and 2 must not both be Dead Ends. One attempt per day.",
   "From Day 2, DR is set to Commonplace until you reach Room 46 or unlock the West Gate.",
   "Morning Room outranks it, but only at West Pierce and East Pierce. That gap is the only reason Utility Closet ever fires.",
   "Cannot be drafted from Edge or Pierce exits."],
 "Conservatory":["Weighted Room at 15%. Highest priority, so it blocks the other three just by being in the Exit List.",
   "Finding the floorplan activates V Mode on Day 1 if you have drafted 1 room or fewer. You do not have to add it to the pool.",
   "Opening a floorplan on the table commits you to setting Manual Rarity, even if you back out. Manual Rarity permanently overrides Dynamic Rarity."],
 "Morning Room":["Weighted Room at 70%, but only at West Pierce or East Pierce.",
   "Cannot be rotated. Treated as a 3-way with a phantom exit that aligns it to the wall.",
   "Rarity cannot be changed in the Conservatory."],
 "Library":["Replaces the rarity table entirely: 0% Commonplace, 0.01% Standard, 49.99% Unusual, 50% Rare.",
   "Rarity Priority inverts: after the initial roll it checks rarest first.",
   "Always filters out Closet, Storeroom, Bedroom, Boudoir, Guest Bedroom, Nursery, Hallway, Corridor, Courtyard, Lavatory, Maid's Chamber, Gymnasium, Darkroom, Furnace.",
   "Under 2 gems it also filters Attic, Music Room, Trophy Room, Ballroom, Vault, Drafting Studio, Master Bedroom, Passageway, Foyer, Cloister, Showroom, Casino, Throne Room.",
   "At 2+ gems it filters the Tunnel instead.",
   "Slot 2 is a Free Draw at 0 gems, otherwise a Gem Draw. Slot 3 is always a Gem Draw unless the Bookshop appears."],
 "Bookshop":["Only from the Library, and only while carrying 1+ gems, once per day.",
   "Needs the Library drafted 8+ times, or 5+ in V Mode or after Room 46.",
   "Hall Pass in V Mode or post-46 gives an instant 90%, then 60%, so 96% total.",
   "Otherwise: first two times a flat 50%, then by books bought: 0 to 1 books 60%, 2 to 4 books 50%, 5+ books 10%. Realm & Rune does not count.",
   "No placement restrictions of its own."],
 "Boiler Room":["Treated as a 2-way Corner for rotation because one door is sealed by the steam barrier.",
   "Cannot be drafted from any Edge Pierce, nor West Advance, nor East Retreat.",
   "Activating it takes the first duct draw from 25% to 70%, anywhere on the estate. It does not need to be connected to your door.",
   "From Day 17 or after Room 46: 60% chance its DR is set to Standard at day start (the Workshop takes the other 40%).",
   "Gear Wrench pickup sets both Workshop and Boiler Room to Standard."],
 "Workshop":["From Day 17 or after Room 46: 40% chance its DR is set to Standard (Boiler Room takes the other 60%).",
   "Picking up a Battery Pack randomises its DR between Standard and Unusual. Each extra Battery Pack that day flips it to whichever was not picked last.",
   "Gear Wrench pickup sets it to Standard."],
 "Security":["Until the intro cutscene has been seen, Security is treated as a Dead End, cannot rotate, and is barred from every Edge exit. That is what forces the centre-door draft.",
   "It is also removed from the Chamber of Mirrors for that day.",
   "Connector Room for duct draws."],
 "The Foundation":["Cannot be drafted at C8 or any Rank 2 Center tile.",
   "90% chance of being removed from the Center Exit List while drafting into a Rank 3 Center tile.",
   "Entering Rank 4 sets DR to Unusual on Days 7 to 20, or Standard on Day 21+. V Mode or Room 46 forces Unusual on entering Rank 4, which overrides the Day 21 check.",
   "Rarity cannot be changed in the Conservatory."],
 "Chamber of Mirrors":["From Day 10, if you have not reached Room 46, an 8% chance per day that DR is set to Standard.",
   "Counts as a fake Dead End for the Draxus filter."],
 "Coat Check":["From Day 3, if you have not reached Room 46, a 25% chance per day that DR is set to Commonplace.",
   "The first time it is drawn on a day, DR becomes Standard. Drawn again the same day, DR becomes Unusual.",
   "TFMurphy could find no code anywhere implementing the Blue Memo's claim that checking a new item makes it appear more often the next day."],
 "Lavatory":["After 3+ total drafts, a 40% chance per day that DR is set to Unusual. It gets rarer the more you use it."],
 "Guest Bedroom":["After 5+ total drafts, if you have not reached Room 46, a 50% chance per day that DR is set to Standard."],
 "Drafting Studio":["Drafted 4 to 7 times total: DR is set to Rare at day start.",
   "Drafted 8+ times: DR stays Unusual, but a 30% chance of being Blocked from Drafting that day.",
   "On Days 1 and 2 it also has a 95% chance of being Blocked. Activating V Mode on Day 1 does NOT lift that block for Day 1.",
   "Its Classroom variant can be drafted at any exit, unlike the Schoolhouse and Chamber of Mirrors versions."],
 "Master Bedroom":["95% chance of being Blocked from Drafting on Days 1 to 2, skipped by V Mode or Room 46.",
   "If the Foundation has never been drafted, DR is forced to Rare on Days 1 to 9 or until Room 46.",
   "If the Foundation has been drafted, from Day 7 there is a 30% chance DR becomes Standard. When that fires, Billiard Room's DR is set to Unusual at the same moment."],
 "Mail Room":["If a package is waiting for you, DR is set to Commonplace at day start."],
 "Cloister":["Upgraded to any variant: DR is set to Standard at day start.",
   "Cloister of Draxus inverts validation: every non-Dead-End slot rerolls into a Dead End.",
   "Drafting from a Cloister delays Conditional Filter activation by one draft."],
 "Terrace":["Default DR is Rare. Entering Rank 3 sets it to Unusual on Day 1, or Standard from Day 2 with a 40% chance of Commonplace instead."],
 "Aquarium":["The Lab experiment that adds 3 Aquariums sets DR to Commonplace and applies BOTH Minor and Major Rarity Bumps at once. That is a bug: the script fails to check for unset DR, so it jumps straight to the strongest tier.",
   "Electric Eel Aquarium counts as a Powered Room, but a bug means drafting from it never gives a duct draw."],
 "Boudoir":["If Her Ladyship's Chamber is drafted, DR is set to Commonplace.",
   "Cannot be drafted from North or South Edge exits."],
 "Walk-In Closet":["If Her Ladyship's Chamber is drafted, DR is set to Commonplace."],
 "Billiard Room":["Early V Mode tell: it is one of the rooms whose DR is reset, making it Commonplace again.",
   "Secret Garden Key sits behind the dartboard at only 1% on Days 1 to 7. V Mode or Room 46 jumps it straight to the final 20%."],
 "Room 8":["Not drafted by the regular system, so it has no placement restrictions.",
   "Using Key 8 still makes a hidden random draw. You never see it, but it feeds the next draft's Runback Filter.",
   "Added to the Blue Color Filter in 1.7, though this does nothing since it cannot be drafted normally."],
 "Secret Garden":["Not drafted by the regular system.",
   "Using the Secret Garden Key still makes a hidden random draw that feeds the next Runback Filter, and it can eat the Garage or Utility Closet Weighted Room chance for the day. Silver Key does not do this.",
   "Excluded from every Color and Feature list."],
 "Tunnel":["Drafting from a Tunnel forces Tunnel into Slot 1 on the first round only. It overrides Silver and Prism Keys.",
   "Whenever you draft into a Center tile from the west or east, Tunnel is Blocked immediately beforehand. The block only lifts when you next draft a Center Room from the north or south, which makes Tunnel impossible to draft in the Wings until then."],
 "Armory":["Only draftable at North/South Pierce if you hold the Mantle of the Knight.",
   "Added via Ambition of the Pawn instead: no Pierce, but it gains South Edge.",
   "Rarity cannot be changed in the Conservatory."],
 "Classroom":["Only draftable at North/South Pierce as the Drafting Studio version.",
   "The Drafting Studio version uses a different subexit for North/South Edge than the Schoolhouse and Chamber of Mirrors versions, so drafting other Classrooms first can prematurely close that exit.",
   "In the Minor Rarity Bump filter at 3%.",
   "Rarity cannot be changed in the Conservatory."],
 "Greenhouse":["Drafting it activates the Green Color Filter at 40% from your next draft, and upgrades the Patio Filter from 5% to 50%.",
   "1.7: if drafted inside the house, Secret Passage leaves the Patio Filter and moves to the Minor Rarity Bump instead. Drafting it in the Outer Room does not do this.",
   "Blocked from Drafting when drafting north from E1. The block only lifts at another East Advance exit, which unintentionally makes it impossible at any West Retreat exit until then."],
 "Furnace":["Drafting it activates the Red Color Filter at 30% from your next draft.",
   "Sheltered, Shielded, or under a Dowsing Rod, its negatives are disabled, which also stops the Red filter activating.",
   "Powered Room for duct draws."],
 "Secret Passage":["Rooms drafted from it can never enter the Runback Filter, so your next draft starts completely clean. Prism Key does not share this.",
   "Blocked when drafting West/East Advance into Rank 8, or West/East Retreat into Rank 2. The block lifts at any other Advance or Retreat exit.",
   "In the Patio Filter at 5%, or 50% with a Greenhouse. 1.7 moves it to the Minor Rarity Bump if the Greenhouse was drafted inside the house.",
   "Counts as a fake Dead End for the Draxus filter.",
   "Weighted Rooms never appear when drafting from it."],
 "Observatory":["In the Major Rarity Bump filter at 13%."],
 "Commissary":["In the Major Rarity Bump filter at 13%.",
   "Offers 1 of 7 sets, and only if you hold none of the items in it. Invalid sets fall through to the next one down; G falls back to A."],
 "Patio":["Gives its name to the always-on Patio Filter: 5% each for Patio, Veranda, Greenhouse, Morning Room and Secret Passage, rising to 50% with a Greenhouse.",
   "Cannot be rotated. Treated as a 3-way with a phantom exit aligning it to the wall.",
   "Internally the list is called PATIO MORNING, and the Cloister references an unused Patio Luck Bonus. Likely a leftover from a scrapped design."],
 "Locker Room":["Rarity cannot be changed in the Conservatory.",
   "Connector Room for duct draws. Counts as a 3-way for the Silver Key."],
 "Gallery":["Rarity cannot be changed in the Conservatory."],
 "Sauna":["Rarity cannot be changed in the Conservatory."],
 "Veranda":["Rarity cannot be changed in the Conservatory.",
   "In the Patio Filter at 5%, or 50% with a Greenhouse."],
 "Throne Room":["Cannot be rotated. Only draftable from the exit that directly faces the throne.",
   "Upgrading it moves it out of the Black Color Filter and into the Blue one."],
 "Weight Room":["Connector Room for duct draws, and gemless, so Slot 1 duct draws can find it.",
   "In the Southern Cross filter at 40%."],
 "Archives":["Connector Room for duct draws, and gemless, so Slot 1 duct draws can find it.",
   "In the Southern Cross filter at 40%.",
   "Duct Draws ignore the Runback Filter entirely, which is why Archives shows up twice in a row so readily."],
 "Passageway":["In the Southern Cross filter at 40%."],
 "Great Hall":["In the Southern Cross filter at 40%."],
 "Rotunda":["In the Southern Cross filter at 40%. Also permitted by the Mechanical filter despite not being a Mechanical Room."],
 "Vestibule":["In the Southern Cross filter at 40%."],
 "Mount Holly Gift Shop":["After reaching Room 46, the first draft inside the house forces it into Slot 1. Overrides the Silver Key. Using the Secret Garden Key or Key 8 counts as a draft and burns the chance.",
   "The Foundation can place it at North Pierce, where it would not normally appear."],
 "Mechanarium":["Center tiles only. Counts as a 4-way.",
   "In the Mechanical filter at 40%."],
 "Pump Room":["Powered Room for duct draws, and gemless, so Slot 1 duct draws can find it.",
   "In the Mechanical filter at 40%."],
 "Laboratory":["Powered Room for duct draws.",
   "In the Mechanical filter at 40%."],
 "Laundry Room":["Powered Room for duct draws."],
 "Darkroom":["Connector Room for duct draws, and gemless, so Slot 1 duct draws can find it."],
 "Freezer":["Under a cooldown it is removed by the Ignore Filter."],
 "Rumpus Room":["Under a cooldown it is removed by the Ignore Filter."],
 "Storeroom":["Always filtered out in the Library and by Berry Picker."],
 "Spare Room":["Added to the Blue Color Filter in 1.7. Removed from it when upgraded.",
   "Upgrades add it to the matching Color List immediately, but it does not leave the Blue list until the following day."],
 "Vault":["Added to the Blue Color Filter in 1.7."],
 "Dining Room":["Its DR is reset by V Mode activation."],
}
PATCH = {
 "Spare Room":"1.7","Vault":"1.7","The Foundation":"1.7","Throne Room":"1.7",
 "Room 8":"1.7","Greenhouse":"1.7","Secret Passage":"1.7",
 "Office":"1.6","Casino":"1.6","Classroom":"1.6","Garage":"1.6",
}

# --------------------------------------------------------------- chess badges
# EDIT THIS LIST. One entry per room, all 110, alphabetical.
# Set a value and a badge shows on that room's card in the Room reference.
#
#     Pawn    #212121        Bishop  #6fc4be
#     Knight  #816e58        King    #ca1f25
#     Rook    #ffffff        Queen   #2280c4
#
# Accepted values:
#     None                 no badge (default)
#     "Rook"               one badge
#     ["Rook", "Pawn"]     several badges, drawn in order
#
# Names are case-insensitive. An unknown name is skipped at render time and
# logged to the browser console, so a typo cannot break the grid.
# The six colours live in CHESS_PIECES in script.js, not here.
CHESS = {
 "Antechamber":            None,
 "Aquarium":               None,
 "Archives":               None,
 "Armory":                 None,
 "Attic":                  None,
 "Ballroom":               None,
 "Bedroom":                None,
 "Billiard Room":          None,
 "Boiler Room":            None,
 "Bookshop":               None,
 "Boudoir":                None,
 "Bunk Room":              None,
 "Casino":                 None,
 "Chamber of Mirrors":     None,
 "Chapel":                 None,
 "Classroom":              None,
 "Clock Tower":            None,
 "Cloister":               None,
 "Closed Exhibit":         None,
 "Closet":                 None,
 "Coat Check":             None,
 "Commissary":             None,
 "Conference Room":        None,
 "Conservatory":           None,
 "Corridor":               None,
 "Courtyard":              None,
 "Darkroom":               None,
 "Den":                    None,
 "Dining Room":            None,
 "Dormitory":              None,
 "Dovecote":               None,
 "Drafting Studio":        None,
 "Drawing Room":           None,
 "East Wing Hall":         None,
 "Entrance Hall":          None,
 "Foyer":                  None,
 "Freezer":                None,
 "Furnace":                None,
 "Gallery":                None,
 "Garage":                 None,
 "Great Hall":             None,
 "Greenhouse":             None,
 "Guest Bedroom":          None,
 "Gymnasium":              None,
 "Hallway":                None,
 "Her Ladyship's Chamber": None,
 "Hovel":                  None,
 "Kitchen":                None,
 "Laboratory":             None,
 "Laundry Room":           None,
 "Lavatory":               None,
 "Library":                None,
 "Locker Room":            None,
 "Locksmith":              None,
 "Lost & Found":           None,
 "Maid's Chamber":         None,
 "Mail Room":              None,
 "Master Bedroom":         None,
 "Mechanarium":            None,
 "Morning Room":           None,
 "Mount Holly Gift Shop":  None,
 "Music Room":             None,
 "Nook":                   None,
 "Nursery":                None,
 "Observatory":            None,
 "Office":                 None,
 "Pantry":                 None,
 "Parlor":                 None,
 "Passageway":             None,
 "Patio":                  None,
 "Planetarium":            None,
 "Pump Room":              None,
 "Room 46":                None,
 "Room 8":                 None,
 "Root Cellar":            None,
 "Rotunda":                None,
 "Rumpus Room":            None,
 "Sauna":                  None,
 "Schoolhouse":            None,
 "Secret Garden":          None,
 "Secret Passage":         None,
 "Security":               None,
 "Servant's Quarters":     None,
 "Shelter":                None,
 "Showroom":               None,
 "Shrine":                 None,
 "Solarium":               None,
 "Spare Room":             None,
 "Storeroom":              None,
 "Study":                  None,
 "Terrace":                None,
 "The Foundation":         None,
 "The Kennel":             None,
 "The Pool":               None,
 "Throne Room":            None,
 "Tomb":                   None,
 "Toolshed":               None,
 "Trading Post":           None,
 "Treasure Trove":         None,
 "Trophy Room":            None,
 "Tunnel":                 None,
 "Utility Closet":         None,
 "Vault":                  None,
 "Veranda":                None,
 "Vestibule":              None,
 "Walk-In Closet":         None,
 "Weight Room":            None,
 "West Wing Hall":         None,
 "Wine Cellar":            None,
 "Workshop":               None,
}

OUTER = ["Toolshed","Shelter","Schoolhouse","Shrine","Root Cellar","Hovel","Trading Post","Tomb"]
OUTER_IMG = {"Toolshed":"Toolshed","Shelter":"Shelter","Schoolhouse":"Schoolhouse","Shrine":"Shrine",
 "Root Cellar":"RootCellar","Hovel":"Hovel","Trading Post":"TradingPost","Tomb":"Tomb"}
OUTER_COLOR = {"Toolshed":["Blueprint"],"Shelter":["Blueprint"],"Schoolhouse":["Blueprint"],
 "Shrine":["Blueprint"],"Root Cellar":["Green Room"],"Hovel":["Bedroom"],
 "Trading Post":["Shop"],"Tomb":["Blackprint"]}
OUTER_NOTES = {
 "Tomb":["45% chance of being pushed to slot 8 of the Outer Room list. V Mode activation or Room 46 drops it to 10%.",
   "V Mode activation on Day 1 and Room 46 both drop it to 10%. Room 46 makes that permanent.",
   "Black Color Filter or Draxus Filter moves it to slot 1, applied last, so it overrides everything else."],
 "Schoolhouse":["45% chance of being pushed to slot 7. V Mode activation or Room 46: 10%.",
   "V Mode activation on Day 1 and Room 46 both drop it to 10%. Room 46 makes that permanent.",
   "Activates the Classrooms filter at 35% for Classroom, Dormitory and Library."],
 "Shrine":["30% chance of being pushed to slot 6. V Mode activation or Room 46: 10%.",
   "V Mode activation on Day 1 and Room 46 both drop it to 10%. Room 46 makes that permanent."],
 "Root Cellar":["Forced to slot 1 by the Green Color Filter, which a Greenhouse also activates."],
 "Hovel":["Forced to slot 1 by the Violet Color Filter."],
 "Trading Post":["Forced to slot 1 by the Yellow Color Filter."],
 "Toolshed":["Part of the first-time-drafting rig with Root Cellar and Hovel, forced to slots 1 to 3. Activating V Mode on Day 1 and then drafting the Outer Room that same day skips this permanently.",
   "Blue Color Filter, branch A: moved to slots 1 to 3 with Shelter and Shrine. Branch B: 50% chance of being moved to slot 1 afterwards."],
 "Shelter":["Blue Color Filter moves it to the front in both branches."],
}

EXTRA = ["Entrance Hall","Antechamber","Room 46","Room 8","Secret Garden","Bookshop"]

# ---------------------------------------------------------------- assemble
names = set(WING) | set(NS) | set(W) | set(DR_DEFAULT) | set(WEEK1) | set(VMODE) | set(NOTES)
names |= set(OUTER) | set(EXTRA)
names -= {""}

def slug(n):
    return (n.replace("'","").replace("&","And").replace("-","")
             .replace(" ","").replace(".",""))

IMG_OVERRIDE = {"Lost & Found":"Lost&Found","Walk-In Closet":"WalkinCloset"}

rooms = []
for n in sorted(names):
    w = W.get(n)
    w0 = W0.get(n)
    img = IMG_OVERRIDE.get(n) or (w[0] if w else OUTER_IMG.get(n) or slug(n))
    is_outer = n in OUTER
    if w:
        colors, gems, base = w[1], w[2], w[3]
    elif w0:
        colors, gems, base = w0[0], 0, w0[1]
    else:
        colors = OUTER_COLOR.get(n, [])
        gems = 0 if is_outer else None
        # every Outer Room sits in Category:Unusual rarity rooms on the wiki
        base = "Unusual" if is_outer else None

    # placement
    place = []
    if is_outer:
        place.append("Outer Room. No placement restrictions apply out here.")
    elif n in ("Entrance Hall","Antechamber","Room 46"):
        place.append("Preplaced. Never drafted.")
    elif n in ("Room 8","Secret Garden"):
        place.append("Not drafted by the regular system, so the Exit Lists do not apply.")
    elif n == "Bookshop":
        place.append("No placement restrictions. Library only.")
    else:
        we, ee, wep = WING.get(n, ("","",""))
        nse, nsp = NS.get(n, ("",""))
        bits = []
        if n in NO_CENTER: bits.append("no Center tiles")
        else: bits.append("Center OK")
        wing_bits = []
        if we: wing_bits.append("West " + ("edge" if we == "O" else we))
        if ee: wing_bits.append("East " + ("edge" if ee == "O" else ee))
        if wep: wing_bits.append("W/E Pierce" if wep == "O" else wep + " Pierce")
        bits.append("Wings: " + (", ".join(wing_bits) if wing_bits else "none"))
        ns_bits = []
        if nse: ns_bits.append(nse if nse != "O" else "N/S Edge")
        if nsp: ns_bits.append("N/S Pierce" if nsp == "O" else nsp)
        bits.append("N/S: " + (", ".join(ns_bits) if ns_bits else "none"))
        bits.append("Corner " + ("OK" if n in CORNER_OK else "no"))
        place.append(". ".join(bits) + ".")

    dyn = DR_DEFAULT.get(n)
    wk = WEEK1.get(n)
    vm = VMODE.get(n)

    rooms.append({
        "n": n, "img": img, "colors": colors, "gems": gems,
        "chess": CHESS.get(n),
        "base": base, "dyn": dyn, "week1": wk, "vmode": vm,
        "outer": is_outer, "place": place,
        "notes": (NOTES.get(n, []) + OUTER_NOTES.get(n, [])),
        "patch": PATCH.get(n),
        "src": {"gems": "W" if (w or w0 or is_outer) else "?",
                "base": "W" if (w or w0 or is_outer) else "?",
                "color": "W" if (w or w0 or is_outer) else "?",
                "place": "T" if (n in WING or n in NS) else "T"},
    })

out = io.StringIO()
out.write("/* Generated by gen_rooms.py. Do not hand-edit.\n")
out.write("   Sources: W = blueprince.wiki.gg tables, T = TFMurphy datamining, ? = not yet sourced. */\n")
out.write("window.ROOMS = ")
json.dump(rooms, out, ensure_ascii=False, separators=(",", ":"))
out.write(";\n")

import os
os.makedirs("out/assets", exist_ok=True)
open("out/assets/rooms-data.js", "w", encoding="utf-8").write(out.getvalue())

known_c = sum(1 for r in rooms if r["colors"])
known_g = sum(1 for r in rooms if r["gems"] is not None)
known_b = sum(1 for r in rooms if r["base"])
print(f"{len(rooms)} rooms written")
print(f"  colors known : {known_c}/{len(rooms)}")
print(f"  gem cost     : {known_g}/{len(rooms)}")
print(f"  base rarity  : {known_b}/{len(rooms)}")
print(f"  dyn rarity   : {sum(1 for r in rooms if r['dyn'] or r['week1'] or r['vmode'])}/{len(rooms)}")
print("\nStill needs colour + base rarity from the wiki:")
print("  " + ", ".join(r["n"] for r in rooms if not r["colors"]))