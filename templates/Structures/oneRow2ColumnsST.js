export function oneRow2Columns(image1, alt1, image2, alt2) {
    return `<div class="container-fluid mb-3">
        <div class="row"">
            <div class="R1C2div col-12 col-lg-6 mb-1">
                <div class="div0R0C">
                    <img class="R1C2image" src="${image1}" alt="${alt1}">
                </div>
            </div>
            <div class="R1C2div col-12 col-lg-6">
                <div class="div0R1C">
                    <img class="R1C2image" src="${image2}" alt="${alt2}">
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
