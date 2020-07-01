function crack(){
	var startCrackingButton = document.getElementById("startCracking");
	startCrackingButton.classList.add("is-loading");

	var attackMode = document.getElementById("attackMode").value
	var hashType = document.getElementById("hashType").value
	var hashes = document.getElementById("hashes").value

	var hashesData = new FormData()
	hashesData.append('hashes', hashes)
	fetch('/api/crack/'+hashType+'/'+attackMode, {
		method: 'POST',
		headers: {
            'X-CSRFToken': csrftoken
        },
		body: hashesData
	})
	.then(response => response.json())
	.then(jsonData => {
		//console.log(jsonData)
		if(jsonData.id){
			window.location.href = "/status/"+jsonData.id;
		}
	})
	.catch(err => {
		//error block
	})
}

function status(crackTaskId){
	var statusSocket = new WebSocket('ws://' + window.location.host + '/ws/task/' + crackTaskId);
    statusSocket.onmessage = function(e) {
		
		var crackingStatus = JSON.parse(e.data);
    	if(crackTaskId == 0){
    		crackTaskId = crackingStatus.id
    	}
        
        switch (crackingStatus.type) {
        	case 'status':

				document.getElementById("crackingProgress-"+crackTaskId).value = crackingStatus.dict.progressPercent
				document.getElementById("crackingPercentage-"+crackTaskId).textContent = crackingStatus.dict.progressPercent+"%"
				document.getElementById("crackingStatus-"+crackTaskId).textContent = crackingStatus.dict.statusText
				document.getElementById("estimatedTime-"+crackTaskId).textContent = crackingStatus.dict.estimatedTime+"s"
				document.getElementById("recoveredHashes-"+crackTaskId).textContent = crackingStatus.dict.recoveredHashes
				try {
					document.getElementById("triedPasswords-"+crackTaskId).textContent = crackingStatus.dict.triedPasswords
					document.getElementById("speed-"+crackTaskId).textContent = crackingStatus.dict.speed+" H/s"
				} catch(e) {
					console.log(e);
				}
					
				
				if(crackingStatus.dict.status!=0 && crackingStatus.dict.status!=3){
					statusSocket.close();
				}
        		break;
        	case 'password':
        		try {
        			crackingStatus.hash_ids.forEach( function(hash_id) {
	        			document.getElementById(hash_id).textContent = crackingStatus.password
	        		});
        		} catch(e) {
        			// statements
        			console.log(e);
        		}
	        		
        		break;
        	default:
        		// statements_def
        		break;
        }


    };

    statusSocket.onclose = function(e) {
        console.error('Socket closed unexpectedly');
    };
}



// function status(crackTaskId){
// 	function statusRequest(crackTaskId, timer){
// 		fetch('/api/crack_status/'+crackTaskId, {
// 			method : 'GET'
// 		})
// 		.then(response => response.json())
// 		.then(crackingStatus => {
// 			if(crackingStatus.status!=0 && crackingStatus.status!=3){
// 				clearInterval(timer);
// 			}

// 			document.getElementById("crackingProgress").value = crackingStatus.progressPercent
// 			document.getElementById("crackingStatus").textContent = crackingStatus.statusText
// 			document.getElementById("crackingPercentage").textContent = crackingStatus.progressPercent+"%"
// 			document.getElementById("recoveredHashes").textContent = crackingStatus.recoveredHashes
// 			document.getElementById("triedPasswords").textContent = crackingStatus.triedPasswords
// 			document.getElementById("speed").textContent = crackingStatus.speed+" H/s"
// 			document.getElementById("estimatedTime").textContent = crackingStatus.estimatedTime+"s"

// 		})
// 		.catch(err => {
// 			// test
// 		})
// 	};
// 	timer = setInterval(function(){statusRequest(crackTaskId, timer)}, 3000);
// }
