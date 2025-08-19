<script>
document.getElementById('apiTestForm').addEventListener('submit', async function(e){
    e.preventDefault();

    const clientId = document.getElementById('clientId').value;
    const nomenclatureId = document.getElementById('nomenclatureId').value;

    const token = 'YOUR_ACCESS_TOKEN_HERE';  // JWT tokenni backenddan olingan holda yozing

    const data = {
        client_id: clientId,
        nomenclature: {
            id: nomenclatureId,
            products: [
                {
                    code: "P001",
                    code1C: "1234",
                    name: "Test Product",
                    catalog_code: "C001",
                    barcode: "1234567890",
                    package_code: "PKG001"
                }
            ]
        }
    };

    try {
        const response = await fetch('/api/integrations/nomenclature/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        document.getElementById('apiResult').innerText = JSON.stringify(result, null, 2);
    } catch (error) {
        document.getElementById('apiResult').innerText = 'Error: ' + error;
    }
});
</script>
