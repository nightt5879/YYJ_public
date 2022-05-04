import numpy as np
import cv2
import csv, os


class Datasets():
    def __init__(self):
        return

    def get_Built_data(self,name):
        print("开始加载数据集")
        from sklearn import datasets
        data_name = name
        if data_name=='digits':
            self.data=datasets.load_digits()
            self.X=self.data.data
            self.Y=self.data.target
            print("手写数字数据集加载完毕")

        elif data_name=='iris':
            self.data=datasets.load_iris()
            self.X = self.data.data
            self.Y = self.data.target
            print("鸢尾花数据集加载完毕")

        elif data_name=='breast_cancer':
            self.data=datasets.load_breast_cancer()
            self.X = self.data.data
            self.Y = self.data.target
            print("乳腺癌数据集加载完毕")

        elif data_name=='diabetes':
            self.data=datasets.load_diabetes()
            self.X = self.data.data
            self.Y = self.data.target
            print("糖尿病数据集加载完毕")

        elif data_name=='boston':
            self.data=datasets.load_boston()
            self.X = self.data.data
            self.Y = self.data.target
            print("房价数据集加载完毕")

        elif data_name=='linnerud':
            self.data=datasets.load_linnerud()
            self.X = self.data.data
            self.Y = self.data.target
            print("体能数据集加载完毕")

    #从csv文件读取其他数据
    def csv_read(self,csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            label = [row[0] for row in reader]
            f.seek(0)
            num = [row[1:] for row in reader]
            Y = label[1:]
            X = num[1:]

            Y = np.array(Y)
            X = np.array(X)

            self.Y = Y.astype(np.int32)
            self.X = X.astype(np.int32)
            self.data = [self.X, self.Y]
            print("csv文件数据读取完毕")

    def data_get(self):
        return self.X,self.Y

    # 对数据集进行划分
    def split(self,test_size):
        from sklearn.model_selection import train_test_split
        self.Xtrain,  self.Xtest,  self.Ytrain,  self.Ytest = train_test_split(self.X, self.Y, test_size=test_size/100);
        print("数据集划分结束，其中测试集占" + str(test_size))
        return

    def split_get(self):
        return self.Xtrain, self.Ytrain, self.Xtest, self.Ytest

    def MinMaxScaler(self):
        from sklearn.preprocessing import MinMaxScaler
        self.X = MinMaxScaler().fit_transform(self.X)
        print('数据归一化完成')
        return self.X

    def StandardScaler(self):
        from sklearn.preprocessing import StandardScaler
        self.X = StandardScaler().fit_transform(self.X)
        print('数据标准化完成')
        return self.X

    def VarianceThreshold(self, k=0):
        from sklearn.feature_selection import VarianceThreshold
        self.X = VarianceThreshold(k).fit_transform(self.X)
        print('数据方差过滤完成')
        return self.X

    def chi2(self,k):
        from sklearn.feature_selection import SelectKBest
        from sklearn.feature_selection import chi2
        self.X = SelectKBest(chi2, k=k).fit_transform(self.X)
        print('数据相关性过滤完成')
        return self.X

    def PCA(self,k):
        from sklearn.decomposition import PCA
        self.X = PCA(n_components=k).fit_transform(self.X)
        print('数据PCA过滤完成')
        return self.X


class DecisionTreeClassifier():
    def __init__(self,max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, random_state=None, max_leaf_nodes=None):
        from sklearn import tree
        self.clf = tree.DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf
                                               ,min_weight_fraction_leaf=min_weight_fraction_leaf, random_state=random_state, max_leaf_nodes=max_leaf_nodes)

    def fit(self, x, y):
        print('开始训练，可能花费较长时间')
        self.fit_=self.clf.fit(x, y)
        print('训练完成')
        return self.fit_

    def score(self, x, y):
        self.the_score=self.clf.score(x, y)
        print('模型验证完成')
        return

    def get_score(self):
        return self.the_score

    def cross_val_score(self,X,Y):
        from sklearn.model_selection import cross_val_score
        self.cross_val_score_=cross_val_score(self.clf,X,Y,cv=5).mean()
        print('交叉验证完成')
        return

    def get_cross_val_score(self):
        return self.cross_val_score_

    def predict(self,X_test,n):
        a=self.clf.predict(X_test)
        return a[n-1]

    def model_save(self,path):
        from joblib import dump
        model_path=path+'.joblib'
        dump(self.clf, model_path)
        print('保存成功')


class RandomForestClassifier():
    def __init__(self,n_estimators=10, max_depth=30):
        from sklearn.ensemble import RandomForestClassifier
        self.clf = RandomForestClassifier (n_estimators=n_estimators, max_depth=max_depth)

    def fit(self, x, y):
        print('开始训练，可能花费较长时间')
        self.fit_=self.clf.fit(x, y)
        print('训练完成')
        return self.fit_

    def score(self, x, y):
        self.the_score=self.clf.score(x, y)
        print('模型验证完成')
        return

    def get_score(self):
        return self.the_score

    def cross_val_score(self,X,Y):
        from sklearn.model_selection import cross_val_score
        self.cross_val_score_=cross_val_score(self.clf,X,Y,cv=5).mean()
        print('交叉验证完成')
        return

    def get_cross_val_score(self):
        return self.cross_val_score_

    def predict(self,X_test,n):
        a=self.clf.predict(X_test)
        return a[n-1]

    def model_save(self,path):
        from joblib import dump
        model_path=path+'.joblib'
        dump(self.clf, model_path)
        print('保存成功')


class KNeighborsClassifier():
    def __init__(self,n_neighbors=5):
        from sklearn.neighbors import KNeighborsClassifier
        self.clf = KNeighborsClassifier(n_neighbors=n_neighbors)

    def fit(self, x, y):
        print('开始训练，可能花费较长时间')
        self.fit_=self.clf.fit(x, y)
        print('训练完成')
        return self.fit_


    def score(self, x, y):
        self.the_score=self.clf.score(x, y)
        print('模型验证完成')
        return

    def get_score(self):
        return self.the_score

    def cross_val_score(self,X,Y):
        from sklearn.model_selection import cross_val_score
        self.cross_val_score_=cross_val_score(self.clf,X,Y,cv=5).mean()
        print('交叉验证完成')
        return

    def get_cross_val_score(self):
        return self.cross_val_score_

    def predict(self,X_test,n):
        a=self.clf.predict(X_test)
        return a[n-1]

    def model_save(self,path):
        from joblib import dump
        model_path=path+'.joblib'
        dump(self.clf, model_path)
        print('保存成功')


class MultinomialNB():
    def __init__(self,alpha=1.0):
        from sklearn.naive_bayes import MultinomialNB
        self.clf = MultinomialNB(alpha=alpha)

    def fit(self, x, y):
        print('开始训练，可能花费较长时间')
        self.fit_=self.clf.fit(x, y)
        print('训练完成')
        return self.fit_

    def score(self, x, y):
        self.the_score=self.clf.score(x, y)
        print('模型验证完成')
        return

    def get_score(self):
        return self.the_score

    def cross_val_score(self,X,Y):
        from sklearn.model_selection import cross_val_score
        self.cross_val_score_=cross_val_score(self.clf,X,Y,cv=5).mean()
        print('交叉验证完成')
        return

    def get_cross_val_score(self):
        return self.cross_val_score_

    def predict(self,X_test,n):
        a=self.clf.predict(X_test)
        return a[n-1]

    def model_save(self,path):
        from joblib import dump
        model_path=path+'.joblib'
        dump(self.clf, model_path)
        print('保存成功')


class LogisticRegression():
    def __init__(self,penalty='l2',r=1):
        from sklearn.linear_model import LogisticRegression
        if penalty=='l1':
            solver='liblinear'
        else:
            solver = 'lbfgs'
        self.clf = LogisticRegression(penalty=penalty,C=1,solver=solver)

    def fit(self, x, y):
        print('开始训练，可能花费较长时间')
        self.fit_=self.clf.fit(x, y)
        print('训练完成')
        return self.fit_

    def score(self, x, y):
        self.the_score=self.clf.score(x, y)
        print('模型验证完成')
        return

    def get_score(self):
        return self.the_score

    def cross_val_score(self,X,Y):
        from sklearn.model_selection import cross_val_score
        self.cross_val_score_=cross_val_score(self.clf,X,Y,cv=5).mean()
        print('交叉验证完成')
        return

    def get_cross_val_score(self):
        return self.cross_val_score_

    def predict(self,X_test,n):
        a=self.clf.predict(X_test)
        return a[n-1]

    def model_save(self,path):
        from joblib import dump
        model_path=path+'.joblib'
        dump(self.clf, model_path)
        print('保存成功')


class SVM():
    def __init__(self,kernel="rbf"):
        from sklearn.svm import SVC
        self.clf = SVC(C=1.0,kernel=kernel,degree=1)

    def fit(self, x, y):
        print('开始训练，可能花费较长时间')
        self.fit_=self.clf.fit(x, y)
        print('训练完成')
        return self.fit_

    def score(self, x, y):
        self.the_score=self.clf.score(x, y)
        print('模型验证完成')
        return

    def get_score(self):
        return self.the_score

    def cross_val_score(self,X,Y):
        from sklearn.model_selection import cross_val_score
        self.cross_val_score_=cross_val_score(self.clf,X,Y,cv=5).mean()
        print('交叉验证完成')
        return

    def get_cross_val_score(self):
        return self.cross_val_score_

    def predict(self,X_test,n):
        a=self.clf.predict(X_test)
        return a[n-1]

    def model_save(self,path):
        from joblib import dump
        model_path=path+'.joblib'
        dump(self.clf, model_path)
        print('保存成功')


class Model_load:
    def __init__(self,path):
        from joblib import load
        model_path = path + '.joblib'
        # print(model_path)
        self.clf = load(model_path)
        print('模型加载完成')

    def fit(self, x, y):
        return self.clf.fit(x, y)

    def score(self, x, y):
        self.the_score = self.clf.score(x, y)
        return

    def get_score(self):
        return self.the_score

    def predict(self,X_test,n):
        a=self.clf.predict(X_test)
        return a[n-1]

    def cross_val_score(self,X,Y):
        from sklearn.model_selection import cross_val_score
        self.cross_val_score_=cross_val_score(self.clf,X,Y,cv=5).mean()
        print('交叉验证完成')
        return

    def get_cross_val_score(self):
        return self.cross_val_score_


def pic2csv(pic_path,csv_path):
    ##获取文件夹名称
    num = []
    for fn in os.listdir(pic_path):
        if '.' not in fn:
            num.append(fn)
    ##路径
    csv_path=csv_path+'.csv'
    ##处理csv文档
    with open(csv_path, "w", newline="")as f:
        # 设置csv文件的列名
        column_name = ["label"]
        column_name.extend(["pixel%d" % i for i in range(64 * 64)])
        # 将列名写入到csv文件中
        writer = csv.writer(f)
        writer.writerow(column_name)
        for i in num:
            # 获取目录的路径
            img_temp_dir = pic_path+'/'+i
            # print(img_temp_dir)
            # 获取该目录下所有的文件
            img_list = os.listdir(img_temp_dir)
            # 遍历所有的文件名称
            for img_name in img_list:
                img = cv2.imread(img_temp_dir + '/' + img_name)
                # print(img_temp_dir + '/' + img_name)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)##灰度
                img1 = cv2.resize(gray, (64, 64), interpolation=cv2.INTER_AREA)
                matrix = np.asarray(img1)
                data = [num.index(i)]
                matrix1 = matrix.flatten()
                data.extend(matrix1)
                # print(data)
                writer.writerow(data)
            print('{:}为{:}'.format(num.index(i),i))
    print('csv写入完成')


def picshow(pic_path,j):
    k=0
    num = []
    for fn in os.listdir(pic_path):
        if '.' not in fn:
            num.append(fn)
    for i in num:
        # 获取目录的路径
        img_temp_dir = pic_path+'/'+i
        # print(img_temp_dir)
        # 获取该目录下所有的文件
        img_list = os.listdir(img_temp_dir)
        # 遍历所有的文件名称
        for img_name in img_list:
            k=k+1
            if k==j:
                img = cv2.imread(img_temp_dir + '/' + img_name)
                cv2.imshow(winname="第{:}张图片".format(j), mat=img)
                cv2.waitKey(2000)
                break


def viedo_to_photo(n,pic_num,img_path,img_name):
    i=0
    #创建文件夹
    path_ = img_path + '/' + img_name
    if not os.path.exists(path_):
        os.mkdir(path_)
    cap = cv2.VideoCapture(n)
    while True:
        if i >= pic_num:
            cv2.destroyAllWindows()
            break
        ret,frame=cap.read()
        if ret==1:
            cv2.imshow("img", frame)
            cv2.imwrite(img_path+'/'+img_name+'/{:}.jpg'.format(i),frame)
        cv2.waitKey(50)
        i=i+1