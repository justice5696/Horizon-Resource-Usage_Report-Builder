##############################################################################################################################################
######################################################### Fill in these fields ###############################################################
##############################################################################################################################################
$pathToScript = "<FILL IN - FOLDER LOCATION OF THE HRUC.py SCRIPT>"
$scriptName = "HRUC.py"
$configFile = "<FILL IN - PATH TO INI CONFIG FILE>"
$scriptPath = "$($pathToScript)\$($scriptName)"
$pathToShare = "<FILL IN - LOCATION WHERE ALL GENERATED REPORTS WILL BE MOVED TO>"
$timebetweenreports_seconds = 43200 # 12 hours is the default
##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################

$date = Get-Date -Format "yyyyMMdd-HHmmss"
$day,$time = $date.split('-')[0,1]
$filename_prefix = "HorizonResourceUsage_"

do {

    Write-Host "Starting the python script at time: $($date)`n`n`n`n`n`n`n" -ForegroundColor Green
    ### NOW RUN THE PYTHON SCRIPT
    python $scriptPath $configFile
    
    Write-Host "`n`n`n`n`n`n`n Finished the python script! `n`n`n`n`n`n`n`n Moving on to the Powershell Logic" -ForegroundColor Green

    #Gets all the files in the $pathToScript Directory
    $search_results = Get-ChildItem -Path $pathToScript | Where-Object { ((! $_.PSIsContainer))}
    Write-Host "Iterating through all files in the folder $($pathToScript)."
    foreach ($file in $search_results)
    {
        #checks if the files in the $pathToScript hqve the filename_prefix
        Write-Host "Iteration: $($file.name) compared to $($filename_prefix)" -ForegroundColor Green
        #Write-Host "        Comparison: $($file.name -like $filename_prefix)"
        Write-Host "        ComparisonB: $(($file.name).StartsWith($filename_prefix))" -ForegroundColor Green

        if(($file.name).StartsWith($filename_prefix))
        {
            #there is a file in the directory with name "HorizonResourceUsage_"
            Copy-Item $file -Destination $pathToShare
            Write-Host  "Iteration: $($file.name) - should now be in $($pathToShare)" -ForegroundColor Green
            
            ## Gets all file objects from the share
            $share_results = Get-ChildItem -Path $pathToShare | Where-Object { ((! $_.PSIsContainer))}

            foreach ($fule in $share_results)
            {
                #confirms that the file has been copied to the share and deletes it if so
                if ($file.name -eq $fule.name) ### Check if file is in share
                {
                    Write-Host "Checking if the local and remote shares have same files. Iteration: $($file.name) -eq/-ne $($fule.name) " -ForegroundColor Green
                    ## DELETE ITEM IN LOCAL FOLDER
                    $tempPath = "$($pathToScript)\$($file.name)"
                    Remove-Item -Path $tempPath 
                }
            }
        }
    }

    #sleep for 12 hours until running the script next
    Write-Host "Starting to sleep for $($timebetweenreports_seconds) seconds" -ForegroundColor Green
    Start-Sleep -Seconds $timebetweenreports_seconds

} while($true)

#script runs forever 