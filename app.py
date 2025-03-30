const express = require("express");
const cors = require("cors");
const ytdl = require("ytdl-core");

const app = express();
app.use(cors());

app.get("/download", async (req, res) => {
    const videoURL = req.query.url;
    
    if (!ytdl.validateURL(videoURL)) {
        return res.json({ error: "Invalid YouTube URL" });
    }

    try {
        const info = await ytdl.getInfo(videoURL);
        const format = ytdl.chooseFormat(info.formats, { quality: "highestvideo" });

        res.header("Content-Disposition", `attachment; filename="video.mp4"`);
        ytdl(videoURL, { format: format }).pipe(res);
    } catch (error) {
        res.status(500).json({ error: "Error downloading video" });
    }
});

app.listen(5000, () => console.log("Server is running on port 5000"));
