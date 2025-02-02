function toTitleCase(str) {
    // https://stackoverflow.com/a/196991/4723940
    return str.replace(
      /\w\S*/g,
      text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
    );
}

function calculateSpeed(bytes, seconds) {
    const speed = ((bytes / (1024 * 1024)) / seconds).toFixed(2);
    // https://stackoverflow.com/a/15762794/4723940
    return `${speed} MB/s`;
}

const grid = document.querySelector("div.clients-grid");

const libs = [
    // in no particular order,
    "telethon",
    "pyrogram",
    "gogram",
    "hydrogram",
    "pyrotgfork",
    "kurigram",
    "mtkruto",
    // if you feel any specific order,
    // it is merely a coincidence
];
for (const lib of libs) {
    const bu = `https://proxy.teligram.workers.dev/github.com/TelegramPlayGround/bmt/raw/master/outputs/${lib}.json`;
    fetch(bu).then((succ) => succ.text()).then((bm) => {
        const apirbm = JSON.parse(bm);

        const card = document.createElement("div");
        card.setAttribute("class", "client-card");

        const cheader = document.createElement("div");
        cheader.setAttribute("class", "client-header");
        const cheaderh2 = document.createElement("h2");
        cheaderh2.innerText = toTitleCase(lib);
        cheader.appendChild(cheaderh2);

        card.appendChild(cheader);

        const metrics = document.createElement("div");
        metrics.setAttribute("class", "metrics");

        const version = document.createElement("div");
        version.setAttribute("class", "metric");

        const info = document.createElement("div");
        info.setAttribute("class", "metric-info");

        const value = document.createElement("div");
        value.setAttribute("class", "metric-value");
        value.innerText = `v${apirbm.version}`; // ${apirbm.layer}`;
        info.appendChild(value);

        const label = document.createElement("div");
        label.setAttribute("class", "metric-label");
        label.innerText = "Version";
        info.appendChild(label);

        version.appendChild(info);
        metrics.appendChild(version);

        const download = document.createElement("div");
        download.setAttribute("class", "metric");

        const downloadinfo = document.createElement("div");
        downloadinfo.setAttribute("class", "metric-info");

        const downloadvalue = document.createElement("div");
        downloadvalue.setAttribute("class", "metric-value");
        downloadvalue.innerText = calculateSpeed(apirbm.file_size, apirbm.download.time_taken);
        downloadinfo.appendChild(downloadvalue);

        const downloadlabel = document.createElement("div");
        downloadlabel.setAttribute("class", "metric-label");
        downloadlabel.innerText = "Download Speed";
        downloadinfo.appendChild(downloadlabel);

        download.appendChild(downloadinfo);
        metrics.appendChild(download);

        const upload = document.createElement("div");
        upload.setAttribute("class", "metric");

        // const uploadicon = document.createElement("i");
        // uploadicon.setAttribute("class", "fas fa-upload");
        // upload.appendChild(uploadicon);

        const uploadinfo = document.createElement("div");
        uploadinfo.setAttribute("class", "metric-info");

        const uploadvalue = document.createElement("div");
        uploadvalue.setAttribute("class", "metric-value");
        uploadvalue.innerText = calculateSpeed(apirbm.file_size, apirbm.upload.time_taken);
        uploadinfo.appendChild(uploadvalue);

        const uploadlabel = document.createElement("div");
        uploadlabel.setAttribute("class", "metric-label");
        uploadlabel.innerText = "Upload Speed";
        uploadinfo.appendChild(uploadlabel);

        upload.appendChild(uploadinfo);
        metrics.appendChild(upload);

        card.appendChild(metrics);

        grid.appendChild(card);
    }).catch(error => {
        console.log(error);
    });
}
