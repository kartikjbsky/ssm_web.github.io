document.addEventListener('DOMContentLoaded', function() {
    const excelBtn = document.getElementById('excelBtn');
    const excelModal = new bootstrap.Modal(document.getElementById('excelModal'));
    const excelLoader = document.getElementById('excelLoader');
    const excelTableContainer = document.getElementById('excelTableContainer');
    
    excelBtn.addEventListener('click', async function() {
        excelModal.show();
        excelLoader.style.display = 'block';
        excelTableContainer.style.display = 'none';
        
        try {
            const response = await fetch('/get_excel');
            if (!response.ok) throw new Error('Failed to load Excel file');
            const data = await response.arrayBuffer();
            
            const workbook = XLSX.read(data, { type: 'array' });
            const firstSheet = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheet];
            const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
            
            displayExcelData(jsonData);
        } catch (error) {
            console.error('Error:', error);
            alert('Error loading Excel file: ' + error.message);
        } finally {
            excelLoader.style.display = 'none';
            excelTableContainer.style.display = 'block';
        }
    });
    
    function displayExcelData(data) {
        const table = document.getElementById('excelTable');
        table.innerHTML = '';
        
        if (!data.length) {
            const row = table.insertRow();
            const cell = row.insertCell();
            cell.colSpan = 2;
            cell.textContent = 'No data found';
            return;
        }
        
        // Create header
        const headerRow = table.insertRow();
        (data[0] || []).forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText || '';
            headerRow.appendChild(th);
        });
        
        // Create rows
        const startRow = data[0] ? 1 : 0;
        for (let i = startRow; i < data.length; i++) {
            const row = table.insertRow();
            (data[i] || []).forEach(cellText => {
                const cell = row.insertCell();
                cell.textContent = cellText || '';
            });
        }
    }
});