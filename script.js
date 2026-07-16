(function () {
  "use strict";
  var mem = {};
  function put(k, v) {
    try {
      localStorage.setItem(k, v);
    } catch (e) {
      mem[k] = v;
    }
  }
  function get(k) {
    try {
      var v = localStorage.getItem(k);
      return v === null ? (k in mem ? mem[k] : null) : v;
    } catch (e) {
      return k in mem ? mem[k] : null;
    }
  }
  function drop(k) {
    try {
      localStorage.removeItem(k);
    } catch (e) {}
    delete mem[k];
  }

  /* ---- compact mode ---- */
  var cbtn = document.getElementById("compactBtn"),
    clbl = document.getElementById("compactLbl");
  function setCompact(on) {
    document.body.classList.toggle("compact", on);
    cbtn.setAttribute("aria-pressed", on ? "true" : "false");
    clbl.textContent = on ? "Compact mode · on" : "Compact mode";
    on ? put("bp:compact", "1") : drop("bp:compact");
  }
  cbtn.addEventListener("click", function () {
    setCompact(!document.body.classList.contains("compact"));
  });
  if (get("bp:compact") === "1") setCompact(true);

  /* ---- checklists ---- */
  document.querySelectorAll(".check").forEach(function (list) {
    var n = list.dataset.list;
    list.querySelectorAll("input[type=checkbox]").forEach(function (cb) {
      var k = "bp:" + n + ":" + cb.id;
      if (get(k) === "1") cb.checked = true;
      cb.addEventListener("change", function () {
        cb.checked ? put(k, "1") : drop(k);
      });
    });
  });
  document.querySelectorAll("[data-reset]").forEach(function (b) {
    b.addEventListener("click", function () {
      var l = document.querySelector(
        '.check[data-list="' + b.dataset.reset + '"]',
      );
      l.querySelectorAll("input[type=checkbox]").forEach(function (cb) {
        cb.checked = false;
        drop("bp:" + b.dataset.reset + ":" + cb.id);
      });
    });
  });

  /* ---- CALC 1 ---- */
  var SLOT2 = {
    9: [32.32, 41.347, 59.26],
    8: [32.32, 41.347, 59.26],
    7: [15.4, 16.21, 59.26],
    6: [15.4, 16.21, 41.8],
    5: [6, 16.21, 41.8],
    4: [6, 6.9, 22.4],
    3: [0, 6.9, 22.4],
    2: [0, 6.9, 3],
    1: [0, 2, 3],
  };
  var S3R = {
    9: 93.75,
    8: 93.75,
    7: 93.75,
    6: 87.5,
    5: 87.5,
    4: 75,
    3: 75,
    2: 75,
    1: 75,
  };
  function fmt(n) {
    return Math.round(n * 100) / 100 + "%";
  }

  /* ---- shared bar renderer ----
     pct is the 0-100 width. val is the text on the right.
     Clamps so a stray >100 or negative can never blow the track open. */
  function barHTML(label, pct, val) {
    var p = +pct;
    if (!isFinite(p) || p < 0) p = 0;
    if (p > 100) p = 100;
    return (
      '<div class="bar' +
      (p === 0 ? " zero" : "") +
      '"><span>' +
      label +
      '</span><span class="track"><span class="fill" style="width:' +
      p.toFixed(1) +
      '%"></span></span><span class="val">' +
      val +
      "</span></div>"
    );
  }
  function drawBars(el, rows) {
    el.innerHTML = rows
      .map(function (r) {
        return barHTML(r[0], r[1], r[2]);
      })
      .join("");
  }
  function calc1() {
    var rank = +document.getElementById("c1rank").value,
      gems = +document.getElementById("c1gems").value || 0,
      draft = +document.getElementById("c1draft").value || 1,
      round = +document.getElementById("c1round").value || 1,
      rooms = +document.getElementById("c1rooms").value || 0,
      day = +document.getElementById("c1day").value || 1,
      vet = document.getElementById("c1vet").value === "1";
    var col = gems === 0 ? 0 : gems <= 3 ? 1 : 2,
      s2 = SLOT2[rank][col],
      s3,
      note;
    // Slot 3 Rare Check
    if (round >= 3) {
      s3 = 100;
      note =
        "From the 2nd redraw on, Slot 3 always makes a Gem Draw regardless.";
    } else if (rooms < 2) {
      s3 = gems >= 2 ? 20 : 0;
      note =
        "Under 2 rooms drafted: " +
        (gems >= 2 ? "20% (you hold 2+ gems)" : "0% (needs 2+ gems)") +
        " if Slot 2 fails.";
    } else if (rooms < 5 && gems < 2) {
      s3 = 20;
      note = "Under 5 rooms drafted and under 2 gems: 20% if Slot 2 fails.";
    } else {
      s3 = S3R[rank];
      note = "Rank " + rank + " baseline: " + s3 + "% if Slot 2 fails.";
    }
    var s3tot = s2 + (100 - s2) * (s3 / 100);
    // Rare Check -> Gem Draw gate
    var need = vet ? 3 : day === 1 ? 6 : day === 2 ? 5 : day === 3 ? 4 : 0;
    var gd = draft >= need;
    document.getElementById("c1s2").textContent = fmt(s2);
    document.getElementById("c1s3").textContent = fmt(s3tot);
    document.getElementById("c1gd").textContent = gd ? "Yes" : "No";
    document.getElementById("c1gd").style.color = gd ? "#5FD3F3" : "#F0B44B";
    var gate =
      need === 0
        ? "Day 4+, so any Rare Check always becomes a Gem Draw."
        : (vet
            ? "V Mode needs 3+ drafts"
            : "Day " + day + " needs " + need + "+ drafts") +
          ". You are on draft " +
          draft +
          ", so a Rare Check " +
          (gd ? "becomes" : "does NOT become") +
          " a Gem Draw" +
          (gd ? "." : " and you get a Free Draw instead.");
    document.getElementById("c1note").textContent =
      "A Rare Check is not a gem draw. It is a gate that a gem draw has to pass through. Slot 2 rolls off rank " +
      rank +
      " and " +
      (col === 0 ? "0 gems" : col === 1 ? "1-3 gems" : "4+ gems") +
      ". If Slot 2 earns a Rare Check, Slot 3 gets one automatically, so Slot 3 total = " +
      fmt(s2) +
      " + " +
      fmt(100 - s2) +
      " x " +
      s3 +
      "%. " +
      note +
      " " +
      gate;
  }
  [
    "c1rank",
    "c1gems",
    "c1draft",
    "c1round",
    "c1rooms",
    "c1day",
    "c1vet",
  ].forEach(function (id) {
    var e = document.getElementById(id);
    e.addEventListener("input", calc1);
    e.addEventListener("change", calc1);
  });

  /* ---- CALC 2 ---- */
  function calc2() {
    var b = document.getElementById("c2boiler").value === "1",
      p1 = b ? 0.7 : 0.25,
      pn = 0.3,
      dist = [0, 0, 0, 0];
    (function walk(slot, count, prob) {
      if (slot === 3 || count >= 3) {
        dist[count] += prob;
        return;
      }
      var p = count > 0 ? pn : p1;
      walk(slot + 1, count + 1, prob * p);
      walk(slot + 1, count, prob * (1 - p));
    })(0, 0, 1);
    var exp = 0,
      rows = [];
    dist.forEach(function (v, i) {
      exp += v * i;
      rows.push([
        i + " duct draw" + (i === 1 ? "" : "s"),
        v * 100,
        (v * 100).toFixed(1) + "%",
      ]);
    });
    drawBars(document.getElementById("c2bars"), rows);
    document.getElementById("c2exp").textContent = exp.toFixed(2);
  }
  document.getElementById("c2boiler").addEventListener("change", calc2);

  /* ---- CALC 3 ---- */
  (function () {
    var d = [
        ["Commonplace", 60],
        ["Standard", 80],
        ["Unusual", 90],
        ["Rare", 99],
      ],
      w = document.getElementById("c3bars");
    drawBars(
      w,
      d.map(function (r) {
        return [r[0], r[1], r[1] + "% out"];
      }),
    );
  })();

  /* ---- TRADING POST: downgrade ladder, loop avoidance, special key ---- */
  (function () {
    var b;
    b = document.getElementById("tp-bars");
    if (b)
      drawBars(b, [
        ["0 trades", 0, "0%"],
        ["1st to 4th", 30, "30%"],
        ["5th onward", 50, "50%"],
      ]);
    b = document.getElementById("tp-loop");
    if (b)
      drawBars(b, [
        ["Ignore loop", 60, "60%"],
        ["Reroll, same tier", 20, "20%"],
        ["Reroll, tier below", 20, "20%"],
      ]);
    b = document.getElementById("sk-bars");
    if (b)
      drawBars(b, [
        ["Silver first", 30, "30%"],
        ["Sec. Garden 1st", 40, "40%"],
        ["Prism first", 30, "30%"],
      ]);
  })();

  /* ---- CALC 4 : outer room, exact Day1 Veteran figures ---- */
  /* Exact figures, by full enumeration of TFMurphy's documented routine
     (uniform 8-room shuffle -> Tomb 8th / Schoolhouse 7th / Shrine 6th penalty
     rolls -> cyclic 3-per-view). Standard penalty rates are 45 / 45 / 30.
     Day 1 Veteran = V Mode activated, so all three sit at 10% and First Time
     Drafting is skipped.
     The 0-redraw column was already correct; the 1-redraw column was not. */
  var OUT = {
    tomb: [34.73, 68.15, 100],
    trade: [39.16, 76.85, 100],
    either: [63.59, 95.7, 100],
  };
  function calc4() {
    var t = document.getElementById("c4t").value,
      r = Math.max(
        0,
        Math.min(3, +document.getElementById("c4red").value || 0),
      ),
      pin = document.getElementById("c4pin").value === "1",
      out,
      note;
    if (pin) {
      out = 100;
      note =
        "Pinned to slot 1, Draxus / Blackprint-common day pins Tomb; a colour-common day pins Hovel, Root Cellar or Trading Post. Free, no dice.";
    } else if (t === "any") {
      out = (Math.min(8, 3 * (r + 1)) / 8) * 100;
      note =
        "Uniform shuffle: 3 of 8 shown per view, list is cyclic. 2 redraws shows all eight.";
    } else {
      out = OUT[t][Math.min(r, 2)];
      note =
        "Day 1 Veteran figures, exact. These exist because activating V Mode drops the Rare Room Penalty to 10% for the rest of the day. At standard rates Tomb is shoved to slot 8 on 45% of shuffles, Schoolhouse to slot 7 on 45%, Shrine to slot 6 on 30%. 2 redraws is guaranteed, because 3 views of 3 cover a cyclic list of 8. 1 die gives 95.7% for at least one of Tomb or Trading Post, assuming no Archives or Greenhouse.";
    }
    document.getElementById("c4out").textContent =
      Math.round(out * 100) / 100 + "%";
    document.getElementById("c4note").textContent = note;
  }
  ["c4t", "c4red", "c4pin"].forEach(function (id) {
    var e = document.getElementById(id);
    e.addEventListener("input", calc4);
    e.addEventListener("change", calc4);
  });

  /* ---- CALC 5 ---- */
  var GATES = {
      free: [3, 3, 3, 3],
      late: [5, 5, 4, 4],
      mid: [4, 4, 3, 3],
      early: [4, 3, 3, 3],
    },
    RN = ["Commonplace", "Standard", "Unusual", "Rare"];
  function calc5() {
    var grp = document.getElementById("c5grp").value,
      ctx = document.getElementById("c5ctx");
    ctx.disabled = grp === "free";
    var gate = grp === "free" ? GATES.free : GATES[ctx.value];
    var sizes = [
      +document.getElementById("c5a").value || 0,
      +document.getElementById("c5b").value || 0,
      +document.getElementById("c5c").value || 0,
      +document.getElementById("c5d").value || 0,
    ];
    var marked = [],
      i = 0,
      sat = false;
    while (i < 4) {
      marked.push(i);
      if (sizes[i] >= gate[i]) {
        sat = true;
        break;
      }
      i++;
    }
    var el = marked.filter(function (k) {
      return sizes[k] >= 1;
    });
    drawBars(
      document.getElementById("c5bars"),
      RN.map(function (n, k) {
        var p = el.indexOf(k) > -1 ? 100 / el.length : 0;
        return [n, p, p.toFixed(1) + "%"];
      }),
    );
    var note =
      "Gate " +
      gate.join("/") +
      ". Marked: " +
      marked
        .map(function (k) {
          return RN[k];
        })
        .join(" → ") +
      ". ";
    note += sat
      ? RN[marked[marked.length - 1]] + " met its gate, so the climb stopped. "
      : "No deck met its gate, all four marked, proceeds anyway (attempt 2 would fail). ";
    note +=
      el.length === 0
        ? "Nothing has size ≥ 1, the attempt fails and drops to the next rung."
        : "Final pick is uniform across the " +
          el.length +
          " marked deck" +
          (el.length === 1 ? "" : "s") +
          " with at least one card.";
    document.getElementById("c5note").textContent = note;
  }
  ["c5grp", "c5ctx", "c5a", "c5b", "c5c", "c5d"].forEach(function (id) {
    var e = document.getElementById(id);
    e.addEventListener("input", calc5);
    e.addEventListener("change", calc5);
  });

  /* ---- MORA JAI ---- */
  var MJ = [
    {
      name: "Trading Post",
      tone: "c-gold",
      realm: "Arch Aries · yellow",
      sigil: "Items for trade",
      cells: { 0: [1], 3: [2, 5, 7, 8, 9], 5: [3], 7: [4, 6] },
    },
    {
      name: "Master Bedroom",
      tone: "c-purple",
      realm: "+1 step per room in your house",
      sigil: "",
      cells: { 7: [2], 8: [1] },
    },
    {
      name: "Tomb",
      tone: "c-black",
      realm: "Blackprint · outer room",
      sigil: "5 gold per dead end",
      cells: { 1: [4, 5], 3: [6], 4: [1, 2, 3] },
    },
    {
      name: "Lost &amp; Found",
      tone: "c-red",
      realm: "2 rare items",
      sigil: "Lose 1 item on entry",
      cells: { 0: [1], 5: [2, 3], 7: [4] },
    },
    {
      name: "Closed Exhibit",
      tone: "c-red",
      realm: "Fenn Aries · red",
      sigil: "Doors security locked",
      cells: {
        1: [1, 5],
        2: [2, 8],
        3: [6],
        4: [4],
        5: [7],
        6: [10],
        7: [3, 9],
      },
    },
    {
      name: "Treasure Trove",
      tone: "c-black",
      realm: "+5 gold per prior draft",
      sigil: "Area",
      cells: { 0: [4], 1: [5], 4: [1], 5: [3, 6], 6: [7], 8: [2] },
    },
    {
      name: "Solarium",
      tone: "c-green",
      realm: "Unusual &amp; Rare rooms more likely",
      sigil: "",
      cells: { 5: [2], 6: [1, 3, 4] },
    },
    {
      name: "Tunnel",
      tone: "c-orange",
      realm: "Always draws Tunnel here",
      sigil: "",
      cells: { 0: [1], 3: [2, 3, 4] },
    },
  ];
  var NSIZE = [37.5, 29, 24, 21, 20, 19, 17.5, 17.5, 17.5, 16];
  (function () {
    var wrap = document.getElementById("mjgrid");
    MJ.forEach(function (box) {
      var board = "";
      for (var i = 0; i < 9; i++) {
        var v = box.cells[i],
          inner = "";
        if (v)
          v.slice()
            .sort(function (a, b) {
              return a - b;
            })
            .forEach(function (n, k) {
              inner +=
                '<b style="font-size:' +
                NSIZE[Math.min(k, NSIZE.length - 1)] +
                'px">' +
                n +
                "</b>";
            });
        board += '<div class="cell">' + inner + "</div>";
      }
      wrap.insertAdjacentHTML(
        "beforeend",
        '<div class="mj"><div class="mj-card ' +
          box.tone +
          '"><h5>' +
          box.name +
          "</h5>" +
          (box.realm ? '<div class="realm">' + box.realm + "</div>" : "") +
          (box.sigil ? '<div class="sigil">' + box.sigil + "</div>" : "") +
          '</div><div class="board">' +
          board +
          "</div></div>",
      );
    });
  })();

  /* ---- ROOM REFERENCE ---- */
  /* ==============================================================
     CHESS BADGES
     --------------------------------------------------------------
     The per-room assignments live in gen_rooms.py (the CHESS dict)
     and ship inside assets/rooms-data.js as each room's "chess"
     field. Edit them there and re-run gen_rooms.py.

     Only the six colours and glyphs live here, so the look is a
     presentation concern and the data stays in the data file.

     A room's "chess" value may be null, "Rook", or ["Rook","Pawn"].
     Names are case-insensitive; an unknown name is skipped and
     logged, so a typo can't break the grid.
     ============================================================== */
  var CHESS_PIECES = {
    Pawn:   { color: "#212121", glyph: "\u265F" },
    Knight: { color: "#816E58", glyph: "\u265E" },
    Rook:   { color: "#FFFFFF", glyph: "\u265C" },
    Bishop: { color: "#6FC4BE", glyph: "\u265D" },
    King:   { color: "#CA1F25", glyph: "\u265A" },
    Queen:  { color: "#2280C4", glyph: "\u265B" },
  };


  var ROOMS = window.ROOMS || [];
  var PAGE = 5,
    shownCount = PAGE;
  (function () {
    var grid = document.getElementById("roomgrid"),
      q = document.getElementById("rq"),
      col = document.getElementById("rcol"),
      rar = document.getElementById("rrar"),
      gem = document.getElementById("rgem"),
      flag = document.getElementById("rflag"),
      cnt = document.getElementById("rcount"),
      more = document.getElementById("moreBtn");
    var RMAP = {
      Commonplace: "t-com",
      Standard: "t-std",
      Unusual: "t-unu",
      Rare: "t-rare",
    };
    var CMAP = {
      Blueprint: "t-blue",
      Bedroom: "t-purple",
      Hallway: "t-orange",
      "Green Room": "t-green",
      Shop: "t-yellow",
      "Red Room": "t-red",
      Blackprint: "t-black",
    };
    var DUCT = [
      "Garage",
      "Boiler Room",
      "Pump Room",
      "Laboratory",
      "Laundry Room",
      "Furnace",
      "Locker Room",
      "Security",
      "Passageway",
      "Archives",
      "Darkroom",
      "Weight Room",
      "Aquarium",
    ];
    var WEIGHTED = ["Conservatory", "Garage", "Morning Room", "Utility Closet"];
    /* resolve a CHESS entry to canonical piece names, tolerating case
       and stray whitespace so the editable list above stays forgiving */
    var PIECE_KEY = {};
    Object.keys(CHESS_PIECES).forEach(function (k) {
      PIECE_KEY[k.toLowerCase()] = k;
    });
    function pieces(room) {
      var v = room && room.chess;
      if (!v) return [];
      return (Array.isArray(v) ? v : [v])
        .map(function (p) {
          var k = PIECE_KEY[String(p).trim().toLowerCase()];
          if (!k)
            console.warn(
              'CHESS: unknown piece "' + p + '" on room "' + room.n + '"',
            );
          return k;
        })
        .filter(Boolean);
    }
    function chessHTML(room) {
      return pieces(room)
        .map(function (k) {
          var d = CHESS_PIECES[k];
          return (
            '<span class="chess" style="--pc:' +
            d.color +
            '" title="' +
            k +
            '"><span class="pg">' +
            d.glyph +
            "</span>" +
            k +
            "</span>"
          );
        })
        .join("");
    }
    function esc(s) {
      return String(s)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    }
    function hay(r) {
      return (
        r.n +
        " " +
        (r.colors || []).join(" ") +
        " " +
        (r.base || "") +
        " " +
        (r.dyn || "") +
        " " +
        (r.place || []).join(" ") +
        " " +
        (r.notes || []).join(" ") +
        " " +
        pieces(r).join(" ")
      ).toLowerCase();
    }
    function match(r) {
      var s = q.value.trim().toLowerCase();
      if (s && hay(r).indexOf(s) < 0) return false;
      var c = col.value;
      if (c === "__none") {
        if ((r.colors || []).length) return false;
      } else if (c && (r.colors || []).indexOf(c) < 0) return false;
      if (rar.value && r.base !== rar.value) return false;
      if (gem.value !== "" && String(r.gems) !== gem.value) return false;
      var f = flag.value;
      if (f === "dyn" && !(r.dyn || r.week1 || r.vmode)) return false;
      if (f === "notes" && !(r.notes || []).length) return false;
      if (f === "outer" && !r.outer) return false;
      if (f === "weighted" && WEIGHTED.indexOf(r.n) < 0) return false;
      if (f === "duct" && DUCT.indexOf(r.n) < 0) return false;
      if (
        f === "bug" &&
        hay(r).indexOf("bug") < 0 &&
        hay(r).indexOf("oversight") < 0 &&
        hay(r).indexOf("unintent") < 0
      )
        return false;
      return true;
    }
    function card(r) {
      var h = '<div class="room-card">';
      h +=
        '<div class="thumb"><img src="assets/rooms/' +
        r.img +
        '.png" alt="' +
        esc(r.n) +
        '" loading="lazy" ' +
        "onerror=\"this.style.display='none';this.parentNode.insertAdjacentHTML('beforeend','<span class=&quot;ph&quot;>" +
        r.img +
        ".png</span>')\"></div>";
      h +=
        "<h5>" +
        esc(r.n) +
        (r.patch ? '<span class="pb">' + r.patch + "</span>" : "") +
        "</h5>";
      h += '<div class="meta">';
      if ((r.colors || []).length)
        r.colors.forEach(function (c) {
          h +=
            '<span class="tag ' + (CMAP[c] || "t-blue") + '">' + c + "</span>";
        });
      else h += '<span class="sb q">colour not sourced</span>';
      if (r.base)
        h += '<span class="tag ' + RMAP[r.base] + '">' + r.base + "</span>";
      if (r.gems !== null && r.gems !== undefined)
        h +=
          '<span class="tag t-blue">' +
          r.gems +
          " gem" +
          (r.gems === 1 ? "" : "s") +
          "</span>";
      h += chessHTML(r);
      h += "</div>";
      if (r.dyn || r.week1 || r.vmode) {
        h +=
          '<div class="kv"><b>Dynamic rarity</b> <span class="sb t">T</span></div><div class="dr">';
        if (r.dyn) h += "<i>default " + r.dyn + "</i>";
        if (r.week1) {
          ["D1", "D2", "D3-4", "D5-7", "D8+"].forEach(function (l, k) {
            if (r.week1[k]) h += "<i>" + l + " " + r.week1[k] + "</i>";
          });
        }
        if (r.vmode)
          h +=
            '<i style="border-color:#5FD3F3;color:#5FD3F3">V Mode ' +
            r.vmode +
            "</i>";
        h += "</div>";
      }
      (r.place || []).forEach(function (pl) {
        h +=
          '<div class="kv"><b>Placement:</b> ' +
          esc(pl) +
          ' <span class="sb t">T</span></div>';
      });
      if ((r.notes || []).length) {
        h +=
          '<ul class="rnotes">' +
          r.notes
            .map(function (x) {
              return "<li>" + x + "</li>";
            })
            .join("") +
          "</ul>";
      }
      return h + "</div>";
    }
    function render() {
      var list = ROOMS.filter(match);
      grid.innerHTML = list.slice(0, shownCount).map(card).join("");
      cnt.textContent =
        Math.min(shownCount, list.length) +
        " of " +
        list.length +
        " shown  (" +
        ROOMS.length +
        " total)";
      if (list.length > shownCount) {
        more.style.display = "block";
        more.textContent =
          "Show " + Math.min(PAGE * 4, list.length - shownCount) + " more";
      } else if (list.length > PAGE) {
        more.style.display = "block";
        more.textContent = "Collapse";
      } else {
        more.style.display = "none";
      }
    }
    more.addEventListener("click", function () {
      var list = ROOMS.filter(match);
      if (shownCount >= list.length) shownCount = PAGE;
      else shownCount += PAGE * 4;
      render();
      if (shownCount === PAGE)
        document.getElementById("s-rooms").scrollIntoView();
    });
    [q, col, rar, gem, flag].forEach(function (e) {
      e.addEventListener("input", function () {
        shownCount = PAGE;
        render();
      });
      e.addEventListener("change", function () {
        shownCount = PAGE;
        render();
      });
    });
    render();
  })();

  /* ---- raw data toggles ---- */
  document.querySelectorAll("[data-raw]").forEach(function (b) {
    b.addEventListener("click", function () {
      var d = document.getElementById("raw-" + b.dataset.raw);
      var on = d.classList.toggle("on");
      b.textContent = on ? "Hide raw data" : "Show raw data";
    });
  });

  /* ---- SEARCH ---- */
  var qEl = document.getElementById("q"),
    hitEl = document.getElementById("hitcount"),
    sections = [].slice.call(document.querySelectorAll(".sec"));
  function clearMarks(root) {
    root.querySelectorAll("mark").forEach(function (m) {
      m.parentNode.replaceChild(document.createTextNode(m.textContent), m);
    });
    root.normalize();
  }
  function esc(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }
  function markIn(node, re) {
    var count = 0,
      walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, {
        acceptNode: function (n) {
          if (!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
          var p = n.parentNode.nodeName;
          if (p === "SCRIPT" || p === "STYLE" || p === "MARK" || p === "OPTION")
            return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        },
      });
    var nodes = [],
      n;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(function (tn) {
      var txt = tn.nodeValue;
      re.lastIndex = 0;
      if (!re.test(txt)) return;
      re.lastIndex = 0;
      var frag = document.createDocumentFragment(),
        last = 0,
        m;
      while ((m = re.exec(txt)) !== null) {
        if (m.index > last)
          frag.appendChild(document.createTextNode(txt.slice(last, m.index)));
        var mk = document.createElement("mark");
        mk.textContent = m[0];
        frag.appendChild(mk);
        last = m.index + m[0].length;
        count++;
        if (m[0].length === 0) re.lastIndex++;
      }
      if (last < txt.length)
        frag.appendChild(document.createTextNode(txt.slice(last)));
      tn.parentNode.replaceChild(frag, tn);
    });
    return count;
  }
  var opened = [];
  function runSearch() {
    var q = qEl.value.trim();
    opened.forEach(function (d) {
      d.open = false;
    });
    opened = [];
    sections.forEach(function (s) {
      clearMarks(s);
      s.classList.remove("hidden");
    });
    if (qEl.value.trim().length >= 2) {
      var rg = document.getElementById("rq");
      if (rg && rg.value === "") {
        /* leave room grid alone */
      }
    }
    if (q.length < 2) {
      hitEl.textContent = "";
      return;
    }
    var re = new RegExp(esc(q), "gi"),
      total = 0,
      shown = 0;
    sections.forEach(function (s) {
      var c = markIn(s, re);
      total += c;
      if (c === 0) s.classList.add("hidden");
      else {
        shown++;
        s.querySelectorAll("details").forEach(function (d) {
          if (!d.open && d.querySelector("mark")) {
            d.open = true;
            opened.push(d);
          }
        });
      }
    });
    hitEl.textContent =
      total === 0
        ? "no matches"
        : total +
          " match" +
          (total === 1 ? "" : "es") +
          " in " +
          shown +
          " section" +
          (shown === 1 ? "" : "s");
  }
  var t;
  qEl.addEventListener("input", function () {
    clearTimeout(t);
    t = setTimeout(runSearch, 140);
  });
  qEl.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      qEl.value = "";
      runSearch();
    }
  });
  document.addEventListener("keydown", function (e) {
    if (
      (e.key === "/" || ((e.ctrlKey || e.metaKey) && e.key === "k")) &&
      document.activeElement !== qEl &&
      document.activeElement.tagName !== "INPUT"
    ) {
      e.preventDefault();
      qEl.focus();
      qEl.select();
    }
  });

  calc1();
  calc2();
  calc4();
  calc5();
})();