"""English guides for unroller.app/guides/. One guide per search intent; build.py renders them.

Text may contain [link text](/guides/slug/) links. Keep each guide answer-first and honest about
what Unroller does (swiping is free, deleting needs Pro).
"""

GUIDES_INDEX = {
    "title": "iPhone Photo Cleanup Guides | Unroller",
    "description": "Step-by-step guides for freeing up iPhone storage, finding large photos and videos, and cleaning up your camera roll without losing the pictures you love.",
    "h1": "Guides for cleaning up your iPhone photos",
    "intro": "Practical answers to the questions people ask when their iPhone storage fills up. Each guide starts with what the Photos app can do on its own.",
}

GUIDES = [
    {
        "slug": "iphone-storage-full-after-deleting-photos",
        "title": "iPhone Storage Still Full After Deleting Photos? 6 Fixes",
        "description": "Deleted photos stay in Recently Deleted for 30 days and still use space. Here is how to get the storage back, and what to check if the number won't move.",
        "h1": "iPhone storage still full after deleting photos? Here's why and how to fix it",
        "card": "Deleted photos keep using space for 30 days. Six things to check when the storage number won't move.",
        "published": "2026-11-20",
        "intro": [
            "Deleted photos stay on your iPhone for 30 days in the Recently Deleted album, and they keep using storage the whole time. Empty that album first. If the number in Settings still doesn't move, the cause is usually iCloud Photos, a storage figure that hasn't refreshed yet, or something other than photos filling up the phone.",
        ],
        "sections": [
            {
                "h2": "1. Empty Recently Deleted",
                "paras": [
                    "When you delete a photo, iOS moves it to Recently Deleted so you can change your mind. The space only comes back when the 30 days run out or when you delete the items there yourself.",
                ],
                "steps": [
                    "Open the Photos app.",
                    "Tap Collections (Albums on older iOS versions) and scroll down to Utilities.",
                    "Open Recently Deleted and unlock it with Face ID or your passcode.",
                    "Tap Select and choose Delete All. On newer iOS versions it sits in the ⋯ menu.",
                ],
                "after": [
                    "The album is hidden when it is empty, so if you can't find it, there is nothing left to clear.",
                ],
            },
            {
                "h2": "2. Give the storage number time to update",
                "paras": [
                    "Settings > General > iPhone Storage is calculated in the background, and after a big cleanup it can lag behind by hours. A restart often makes iOS recalculate sooner. Check again after restarting before you try anything drastic.",
                ],
            },
            {
                "h2": "3. Let iCloud Photos finish syncing",
                "paras": [
                    "With iCloud Photos turned on, a deletion has to reach iCloud before it settles on every device. Until then, a photo you deleted can show up again because another device still has it. Scroll to the bottom of your library in the Photos app to see the sync status, and leave the iPhone on Wi-Fi and charging for a while so it can finish.",
                ],
            },
            {
                "h2": "4. Turn on Optimize iPhone Storage",
                "paras": [
                    "If you use iCloud Photos, Optimize iPhone Storage keeps smaller versions on the phone and the full originals in iCloud. Turn it on in Settings > your name > iCloud > Photos. It frees space gradually and needs some free space to work, so the Photos number won't drop the same day.",
                    "Don't turn iCloud Photos off to save space. iOS then offers to download every original to the phone, which needs more storage, not less. If you do switch it off, read the prompt carefully: Remove from iPhone deletes the local copies, while Download keeps full copies on the phone.",
                ],
                "cta": True,
            },
            {
                "h2": "5. Find out what is really using the space",
                "paras": [
                    "Settings > General > iPhone Storage lists everything by size. If Photos isn't near the top, deleting more pictures won't help much.",
                    "Messages is a common surprise, because every photo and video in your chats is stored there separately. Tap Messages in that list to review large attachments and old conversations. System Data covers caches and temporary files. You can't delete it directly, and its size changes on its own.",
                ],
            },
            {
                "h2": "6. Delete the files that make a difference",
                "paras": [
                    "If Photos really is the biggest item, a handful of videos usually outweighs hundreds of photos. One minute of 4K video at 60 fps takes about 400 MB in the default High Efficiency format, while a photo is a few megabytes. [Find your largest photos and videos](/guides/sort-iphone-photos-by-size/) first, delete what you don't need, then empty Recently Deleted again.",
                ],
            },
        ],
        "faq": [
            ("How long do deleted photos stay on my iPhone?",
             "They stay in the Recently Deleted album for 30 days, then iOS removes them for good. You can remove them sooner by deleting them from that album."),
            ("Why did photos I deleted come back?",
             "Usually iCloud Photos had not finished syncing the deletion, so another device or iCloud put the photo back. Let the sync finish on Wi-Fi, then delete the photo again if it is still there."),
        ],
        "related": ["sort-iphone-photos-by-size", "clean-up-camera-roll-fast"],
    },
    {
        "slug": "sort-iphone-photos-by-size",
        "title": "How to Sort iPhone Photos by Size and Find Large Files",
        "description": "The Photos app can't sort by file size. Here is how to check sizes, find your biggest videos and list your largest photos and videos in one place.",
        "h1": "How to sort iPhone photos by size and find your largest files",
        "card": "The Photos app can't sort by file size. How to find the photos and videos that take up the most space.",
        "published": "2026-11-20",
        "intro": [
            "The Photos app can't sort your library by file size. You can check the size of one photo or video at a time in its Info panel, and you can filter your library to videos, which are almost always the largest files. To see your biggest files in a single list, you need an app such as Unroller.",
        ],
        "sections": [
            {
                "h2": "Check the size of a single photo or video",
                "steps": [
                    "Open the photo or video in the Photos app.",
                    "Swipe up, or tap the Info button (i).",
                    "The panel shows the file size along with the resolution and camera details.",
                ],
                "after": [
                    "That is useful for checking one suspicious file, but not for finding the largest ones among thousands.",
                ],
            },
            {
                "h2": "Look at your videos first",
                "paras": [
                    "Videos are where the storage goes. One minute of 4K video at 60 fps uses about 400 MB in the default High Efficiency format, while a typical photo is a few megabytes. Slo-mo and Cinematic videos are large for their length too.",
                    "In Photos, tap Collections, scroll to Media Types and open Videos to see only your videos. Each thumbnail shows the length of the clip, which is a decent stand-in for its size.",
                    "Sometimes Settings > General > iPhone Storage also shows a recommendation called Review Personal Videos. It lists your videos by size and lets you delete them right there. It only appears when iOS thinks it will help, and it doesn't include photos.",
                ],
            },
            {
                "h2": "See how much space your whole library uses",
                "paras": [
                    "Open Settings > General > iPhone Storage and tap Photos. The total includes everything in your library plus whatever is still waiting in Recently Deleted. Write the number down before you start, so you can see what the cleanup actually saved. If Photos turns out to be small compared to your apps, sorting photos by size won't free much, and the other items in that list deserve a look first.",
                ],
            },
            {
                "h2": "Sort photos and videos by size with Unroller",
                "paras": [
                    "Unroller has a Big Size category that lists your largest photos and videos first, so you can decide about the files that free the most space.",
                ],
                "steps": [
                    "Open Unroller and allow access to your photos.",
                    "Tap Categories and choose Big Size.",
                    "Swipe left on files you don't need and right on the ones you keep. The counter at the top shows how much space you have marked.",
                    "Review your selection and delete. The files move to Recently Deleted, where you can restore them for 30 days.",
                ],
                "figure": ("en-categories.jpg", "Unroller categories including Big Size for the largest files", "The Big Size category in Unroller lists your largest files first."),
                "cta": True,
            },
            {
                "h2": "Other large files hiding in your library",
                "paras": [
                    "Live Photos store a short video next to each still image, so they take roughly twice the space of a normal photo. Screen recordings are easy to forget and can run to hundreds of megabytes. Duplicates add up quietly as well: Photos collects exact copies in Collections > Utilities > Duplicates, where you can merge them.",
                    "Before you delete a long video you might want later, copy it somewhere else first: AirDrop it to a Mac, or save it to an external drive through the Files app. If you want to keep a video on the phone but not its size, Unroller's video compressor makes a smaller copy.",
                    "Once you've deleted the big files, empty Recently Deleted to get the space back. If the storage number still doesn't change, see [why iPhone storage stays full after deleting photos](/guides/iphone-storage-full-after-deleting-photos/).",
                ],
            },
        ],
        "faq": [
            ("Can I see the total size of several selected photos on iPhone?",
             "Not in the Photos app, which shows the size of one item at a time. In Unroller, the counter at the top shows how much space the photos you marked for deletion take up."),
            ("How do I make iPhone videos smaller in the future?",
             "Go to Settings > Camera > Formats and choose High Efficiency, which takes about half the space of Most Compatible. In Settings > Camera > Record Video, 1080p at 30 fps uses far less space than 4K at 60 fps."),
        ],
        "related": ["iphone-storage-full-after-deleting-photos", "clean-up-camera-roll-fast"],
    },
    {
        "slug": "clean-up-camera-roll-fast",
        "title": "How to Clean Up Your iPhone Camera Roll Fast",
        "description": "Clear screenshots, duplicates and big videos first, then swipe through the rest month by month. A practical order for cleaning up your iPhone camera roll.",
        "h1": "How to clean up your iPhone camera roll fast",
        "card": "Clear the bulk categories first, then go month by month. A practical order that keeps it from taking all weekend.",
        "published": "2026-11-20",
        "intro": [
            "The fastest way to clean up an iPhone camera roll is to clear the bulk categories first (screenshots, duplicates and large videos) and then go through the rest one month at a time, deciding photo by photo. Several short sessions work better than one long one, because you keep making good decisions instead of skipping everything.",
        ],
        "sections": [
            {
                "h2": "Before you start: check your backup and set a few rules",
                "paras": [
                    "Make sure the photos you care about exist somewhere else. With iCloud Photos turned on, remember that deleting on the iPhone deletes in iCloud too, so iCloud is not a backup of what you remove. A copy on a computer or an external drive is.",
                    "Then decide on a few rules so you don't think about every photo from scratch. Keep the best shot of a series and delete the rest. Delete blurry photos unless they're the only picture of a moment. Delete photos you took as notes, like receipts, parking spots or price tags, once you no longer need them. Rules like these turn most decisions into a one-second swipe.",
                ],
            },
            {
                "h2": "1. Delete screenshots in bulk",
                "paras": [
                    "Screenshots pile up faster than anything else, and most of them were only useful for a minute.",
                ],
                "steps": [
                    "In Photos, tap Collections and scroll to Media Types.",
                    "Open Screenshots and tap Select, then Select All.",
                    "Deselect the few you want to keep and tap the trash button.",
                ],
                "after": [
                    "Screen recordings and automatic cleanup are covered in [how to delete all screenshots on iPhone](/guides/delete-all-screenshots-iphone/).",
                ],
            },
            {
                "h2": "2. Merge duplicates",
                "paras": [
                    "Photos finds exact copies for you. Open Collections > Utilities > Duplicates and tap Merge. Photos keeps the best version and moves the extra copies to Recently Deleted. The Duplicates album only appears when Photos has found some. More detail in [how to delete duplicate photos on iPhone](/guides/delete-duplicate-photos-iphone/).",
                ],
            },
            {
                "h2": "3. Clear out the biggest videos",
                "paras": [
                    "A few long videos often take more space than your entire photo collection from a year. [Find your largest photos and videos](/guides/sort-iphone-photos-by-size/) and decide about those before anything else.",
                ],
            },
            {
                "h2": "4. Swipe through the rest month by month",
                "paras": [
                    "What's left are the photos that need a real decision: the twelve near-identical shots of a sunset, the blurry ones, the photos of a parking spot. Selecting them in a grid is slow and tiring. Seeing one photo at a time and deciding with a swipe is much quicker.",
                ],
                "steps": [
                    "Open Unroller and pick a month, starting with the most recent one.",
                    "Swipe left to delete and right to keep. Your choices go into a review list, nothing is deleted yet.",
                    "At the end of the month, check the list and delete the photos you marked.",
                    "Unroller crosses the month off and remembers where you stopped, so you can do one month a day.",
                ],
                "figure": ("en-keep.jpg", "Unroller with a photo swiped right to keep", "Swipe right to keep a photo, left to delete it."),
                "cta": True,
            },
            {
                "h2": "5. Empty Recently Deleted",
                "paras": [
                    "Everything you deleted sits in Recently Deleted for 30 days and still uses storage. When you're done, open Collections > Utilities > Recently Deleted and delete all. If your storage doesn't go down afterwards, read [why iPhone storage stays full after deleting photos](/guides/iphone-storage-full-after-deleting-photos/).",
                ],
            },
            {
                "h2": "Keep the camera roll from filling up again",
                "paras": [
                    "Delete screenshots right after you share them: tap the preview after taking one, tap Done (a check mark on newer iOS versions) and choose Delete Screenshot. In WhatsApp, turn off Settings > Chats > Save to Photos so every image from group chats doesn't land in your library. And when a new month starts, spend five minutes swiping through the last one.",
                ],
            },
        ],
        "faq": [
            ("Is it safe to clean up my camera roll with an app?",
             "Apps that use Apple's Photos framework delete through the same system as the Photos app, so deleted items go to Recently Deleted and stay recoverable for 30 days. Also check that the app processes photos on the device. Unroller never uploads your photos."),
            ("What should I delete first to free up the most space?",
             "Videos, because one long 4K video can be as big as hundreds of photos. After that, duplicates and screenshots, then everything else month by month."),
        ],
        "related": ["iphone-storage-full-after-deleting-photos", "sort-iphone-photos-by-size"],
    },
    {
        "slug": "delete-duplicate-photos-iphone",
        "title": "How to Find and Delete Duplicate Photos on iPhone",
        "description": "Photos finds exact duplicates and merges them in a few taps. Here is how, why the Duplicates album can be missing, and how to handle similar shots.",
        "h1": "How to find and delete duplicate photos on iPhone",
        "card": "Merge exact copies with the built-in Duplicates album, and deal with the near-identical shots it misses.",
        "published": "2026-11-20",
        "intro": [
            "On iOS 16 and later, the Photos app finds duplicate photos for you. Open Collections, scroll to Utilities and tap Duplicates, then tap Merge on each pair or select them all and merge them at once. Photos keeps one copy with the best quality and moves the rest to Recently Deleted. It only catches photos that are identical or almost identical, so similar shots of the same moment need a second pass.",
        ],
        "sections": [
            {
                "h2": "Merge duplicates in the Photos app",
                "steps": [
                    "Open Photos and tap Collections (Albums on older iOS versions).",
                    "Scroll to Utilities and tap Duplicates.",
                    "Tap Merge next to a set, then confirm with Merge Exact Copies or Merge Items.",
                    "To merge everything, tap Select, then Select All, then Merge at the bottom.",
                    "Open Recently Deleted and delete the extra copies to get the space back.",
                ],
                "after": [
                    "Merging is not the same as deleting one copy by hand. Photos combines the information from both items, like album membership and keywords, into the copy it keeps. With iCloud Photos turned on, the merge applies on all your devices.",
                ],
            },
            {
                "h2": "Why the Duplicates album is missing",
                "paras": [
                    "The Duplicates album only appears once Photos has indexed your library and found at least one duplicate. Indexing runs in the background while the iPhone is locked and connected to power, so after an update or a large import it can take a night or two. While it's still running, a status message shows at the bottom of your library.",
                    "If the album never appears, Photos hasn't found anything that counts as a duplicate. Its rules are strict on purpose: it looks for the same image, sometimes in a different resolution or format, not for two photos that just look alike.",
                ],
            },
            {
                "h2": "Clean up similar photos the built-in tool misses",
                "paras": [
                    "Most of the clutter isn't exact copies. It's the eight shots you took to get one good group photo, or the same sunset from slightly different angles. Photos treats those as different pictures and leaves them alone.",
                    "Unroller has a duplicate finder that also groups similar photos, so you see the shots of one moment side by side and can keep only the best one.",
                ],
                "steps": [
                    "Open Unroller and tap Tools.",
                    "Open the Duplicate Detector and tap Review Duplicates.",
                    "Go through the groups and choose which photos to delete.",
                    "Confirm the deletion. The photos go to Recently Deleted for 30 days.",
                ],
                "figure": ("en-tools.jpg", "Unroller tools screen with the duplicate detector and album cleaner", "The duplicate detector in Unroller shows how many duplicates it found and how much space they use."),
                "cta": True,
            },
            {
                "h2": "Bursts and Live Photos",
                "paras": [
                    "Burst photos sit in one stack that looks like a single picture. Open Collections > Media Types > Bursts, open a burst, tap Select, pick the frames you want and tap Done, then choose Keep Only Favorites. Live Photos aren't duplicates, but each one stores a short video next to the photo, so they take roughly twice the space of a normal photo.",
                    "When you're done, empty Recently Deleted. If the storage number doesn't change, read [why iPhone storage stays full after deleting photos](/guides/iphone-storage-full-after-deleting-photos/).",
                ],
            },
        ],
        "faq": [
            ("Does merging duplicates on iPhone lose any photos?",
             "No. Photos keeps the highest-quality version and combines the details of both copies into it. The extra copies go to Recently Deleted, where you can restore them for 30 days. As with any large cleanup, keep a backup before merging hundreds of items."),
            ("Why doesn't my iPhone find all my duplicates?",
             "The built-in tool only flags identical or nearly identical images. Similar photos taken a second apart count as different pictures. For those you need to compare them yourself or use an app that groups similar shots."),
        ],
        "related": ["clean-up-camera-roll-fast", "delete-all-screenshots-iphone"],
    },
    {
        "slug": "delete-all-screenshots-iphone",
        "title": "How to Delete All Screenshots on iPhone at Once",
        "description": "Open the Screenshots album, Select All and delete. Plus how to keep the few you need, clear screen recordings and stop screenshots piling up again.",
        "h1": "How to delete all screenshots on iPhone at once",
        "card": "Clear the Screenshots album in a few taps, keep the ones you still need and stop new ones from piling up.",
        "published": "2026-11-20",
        "intro": [
            "To delete all screenshots on iPhone at once, open Photos, go to Collections > Media Types > Screenshots, tap Select, then Select All, and tap the trash button. Then empty Recently Deleted, because deleted screenshots keep using storage there for 30 days.",
        ],
        "sections": [
            {
                "h2": "Delete every screenshot in a few taps",
                "steps": [
                    "Open the Photos app and tap Collections (Albums on older iOS versions).",
                    "Scroll to Media Types and tap Screenshots.",
                    "Tap Select, then Select All.",
                    "Tap the trash button and confirm.",
                    "Open Collections > Utilities > Recently Deleted and delete them there too.",
                ],
                "after": [
                    "If you have thousands of screenshots, Photos can take a moment to select them all. Wait until the counter at the top stops before you tap the trash button.",
                ],
            },
            {
                "h2": "Keep the screenshots you still need",
                "paras": [
                    "Boarding passes, receipts and confirmation codes are easy to delete by accident. The quick way: before you select everything, mark the few you want to keep as favorites. Then Select All, scroll through and deselect the ones with a heart. Or simply deselect them one by one.",
                    "If you want to decide about each screenshot, swiping is faster than tapping through a grid. In Unroller, open Categories and pick Screenshots, then swipe left to delete and right to keep.",
                ],
                "figure": ("en-delete.jpg", "Unroller with a photo swiped left to delete", "Swipe left to mark a screenshot for deletion, right to keep it."),
                "cta": True,
            },
            {
                "h2": "Don't forget screen recordings",
                "paras": [
                    "Screen recordings live in their own album under Media Types, and they are much larger than screenshots. A few minutes of recording can take hundreds of megabytes. Clear them the same way: open Screen Recordings, tap Select, then Select All, and delete.",
                ],
            },
            {
                "h2": "Find screenshots that aren't in the Screenshots album",
                "paras": [
                    "The Screenshots album only holds screenshots you took on this iPhone. Screenshots that friends sent you in WhatsApp or Messages and that you saved count as normal photos, so they hide in your library between everything else. The same goes for screenshots from an old phone that came over through a computer import.",
                    "Searching helps here. Type a word you remember from the screenshot into the Photos search, like a shop name or \"receipt\", and Photos finds pictures that contain that text. Going through your library month by month catches the rest, because screenshots are easy to spot when you see one picture at a time.",
                ],
            },
            {
                "h2": "Delete old screenshots automatically",
                "paras": [
                    "The Shortcuts app can clean up for you. Create a shortcut with a Find Photos action filtered to Is a Screenshot and a creation date older than 30 days, followed by a Delete Photos action. Run it from a personal automation once a week.",
                    "Two limits: iOS asks you to confirm before Shortcuts deletes photos, so it isn't fully hands-free. And screenshots that someone sent you and you saved don't count as screenshots, so the filter skips them.",
                ],
            },
            {
                "h2": "Stop screenshots from piling up",
                "paras": [
                    "Delete a screenshot right after you've used it: tap the preview after taking it, tap Done (a check mark on newer iOS versions) and choose Delete Screenshot. You can also choose Save to Files for screenshots you want to keep but not see in your photo library.",
                    "For the rest of your camera roll, see [how to clean up your camera roll fast](/guides/clean-up-camera-roll-fast/).",
                ],
            },
        ],
        "faq": [
            ("Does deleting screenshots free up space on iPhone?",
             "Yes, once you also delete them from Recently Deleted. A single screenshot is small, but thousands of them add up, and screen recordings take much more space."),
            ("Can I stop my iPhone from saving screenshots to Photos?",
             "There is no setting that keeps screenshots out of Photos entirely. After taking one, you can tap the preview, tap Done and choose Save to Files or Delete Screenshot instead of saving it to your library."),
        ],
        "related": ["clean-up-camera-roll-fast", "delete-duplicate-photos-iphone"],
    },
]
