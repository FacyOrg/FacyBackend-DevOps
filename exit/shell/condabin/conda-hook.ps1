$Env:CONDA_EXE = "/home/kubernetes/FacyBackend-DevOps/exit/bin/conda"
$Env:_CE_M = ""
$Env:_CE_CONDA = ""
$Env:_CONDA_ROOT = "/home/kubernetes/FacyBackend-DevOps/exit"
$Env:_CONDA_EXE = "/home/kubernetes/FacyBackend-DevOps/exit/bin/conda"
$CondaModuleArgs = @{ChangePs1 = $True}
Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1" -ArgumentList $CondaModuleArgs

Remove-Variable CondaModuleArgs