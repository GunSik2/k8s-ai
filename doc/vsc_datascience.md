# Visual Studio Code 활용한 DataScience 시험

## Code 가상환경 생성
```
conda create -n keras python=3.7 pandas jupyter seaborn scikit-learn keras tensorflow
```

## VSC 환경 구성
- 시험 폴더 생성
- File > Open Folder : 시험 폴더 오픈
- View > Command Palette or Ctrl+Shift+P => Python: Select Interpreter => 'keras': conda
- VSC File Explorer > Noe File : hello.ipynb
- (Jupytern 오픈 : Ctrl+Shift+P > Jupyter: Create New Blank Jupyter Notebook)


## Streamlit 환경
```
conda create -n keras python=3.7 pandas jupyter seaborn scikit-learn keras tensorflow
conda activate keras
pip install streamlit
conda deactivate
```
## 참고자료
- https://code.visualstudio.com/docs/python/data-science-tutorial
- https://www.openml.org/d/40945
