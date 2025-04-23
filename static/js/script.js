//import { oneRow2Columns } from "oneRow2ColumnsT.js"; 

// function oneRow2Columns(image1, alt1, image2, alt2) {
//     return `<div class="container-fluid mb-3">
//         <div class="row"">
//             <div class="R1C2div col-12 col-lg-6">
//                 <div class="div0R0C">
//                     <img class="R1C2image" src="${image1}" alt="${alt1}">
//                 </div>
//             </div>
//             <div class="R1C2div col-12 col-lg-6">
//                 <div class="div0R1C">
//                     <img class="R1C2image" src="${image2}" alt="${alt2}">
//                 </div>
//             </div>
//         </div> 

//         <style>
//             .R1C2image{
//                 border-radius: 0.3rem;
//                 width: 100%;
//                 height: 100%;
//             }
//             .R1C2div{
//                 border-radius: 0.3rem;

//             }
//         </style>
//     </div>
//     `;
// }

function oneRow2Columns(image1, alt1, link1, image2, alt2, link2,  id1="", id2="") {
    return `<div class="container-fluid mb-3">
                <div class="row"">
                    <div class="R1C2div col-12 col-lg-6 position-relative mb-3">
                        <img src="${image1}" class="R1C2image" alt="${alt1}">
                        <div class="rounded-pill border border-primary link-box">
                            <a class="icon-link icon-link-hover text-white text-decoration-none" href="${link1}">
                                Buy Now
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-arrow-right" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
                                </svg>
                            </a>
                        </div>
                    </div>

                    <div class="R1C2div col-12 col-lg-6 position-relative">
                        <img src="${image2}" class="R1C2image" alt="${alt2}">
                        <div class="rounded-pill border border-primary link-box ">
                            <a class="icon-link icon-link-hover text-white text-decoration-none" href="${link2}">
                                Buy Now
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-arrow-right" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
                                </svg>
                                
                            </a>
                        </div>
                    </div>
                </div>

        <style>
            .R1C2image{
                border-radius: 0.3rem;
                width: 100%;
                height: 100%;
            }
            .R1C2div{
                border-radius: 0.3rem;

            }
        </style>
    </div>
    `;
}

function landcapeRow(image, alt){
    return `<div class="container-fluid">
                <div class="row">
                    <div class="col-lg-12">
                        <div class="landscapeDiv">
                            <img class="landscapeImageDiv" src="${image}" alt="${alt}">
                        </div>
                    </div>
                </div>
            </div>`
}
// const mainContent = document.getElementById("JsControlled");

// const div1 = document.createElement("div");
// div1.innerHTML = oneRow2Columns("/static/img/Computers/1980s/AppleLisa/AppleLisa5.jpeg", "Apple Lisa", "./index.html", "/static/img/Computers/1980s/AppleLisa/AppleLisa2.webp", "Apple Lisa", "./login.html");

// mainContent.appendChild(div1);

