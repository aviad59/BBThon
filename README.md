# BBThon
The official repository of the official BIBI language - **BBthon!**
![1018316866_optimized](https://user-images.githubusercontent.com/50523112/120692553-96e7e480-c4b0-11eb-81dd-1f47652c6033.png)

<div align="right">

<div align="center">

# 🎲Tutorial🎲

<div dir="rtl">

אזרחים יקרים שלום, וברוכים הבאים למדריך לשפת ביבי!

שפת ביבי או בשמה הרשמי BBThon נכתבה בשפת פייתון למטרות הומור בלבד. אין בכתיבת השפה מטרה לפגוע בשום אופן או צורה שהיא.

ועכשיו לאחר שהבהרנו את זה בואו נראה על מה מדובר!

</div>

</div>

<div align="center">

## **תוכן עניינים**

</div>

<div align="left">

* ### Requirements

* ### Documentation

* ### About

</div>
<div align="center">

# ⚙️Requirements⚙️

</div>

 על מנת להריץ את ביביתון יש צורך בגרסת פייתון 3.7.1 לפחות
 (גרסאות נמוכות מזו לא נבדקו!)
 
 `shell.py` לאחר העתקת כל הקבצים יש להפעיל באמצעות פייתון את הקובץ 
 
 ```
 python shell.py
 ```
 
 על מנת להריץ קובץ הוראות בביביתון יש לכתוב לאחר מכן את הפקודה הבאה עם שם הקובץ המתאים
 
 ```
 בחירות("שם_הקובץ")
 ```
 
הערה חשובה: הטרמינל במערכות ההפעלה כיום עובד משמאל לימין (ככל הנראה עקב אנטישמיות כמובן) ולכן אין מה לדאוג אם הפקודות נכתבות הפוך
<div align="left">
 
 ```
 BBthon> תוריחב("דוגמה.bb")
 ```
 
</div>

*(: פרוייקט עתידי: טרמינל כשר מימין לשמאל*
 
<div align="center">

# 📁Documentation📁

</div>

שפת ביבי מכילה בתוכה כל מה ששפת תכנות צריכה להכיל!
ממשתנים עד לולאות ומלולאות עד פונקציות הכל 

!כולל הכל
```
~אומר שלום לאזרחים
שרה("אזרחים יקרים")

~ סופר כמות בחירות
בשביל א = 1 עד 5 אז
שרה("בחירות")
סיום

~ פעולה לחישוב כמות מנדטים חסרים
מוחמדף קואליציה(מספר) -> 61 - מספר

~ מתנה מסוג שוחד המייצגת את כמות המנדטים
מתנה מנדטים = 24
~ חישוב כמה מנדטים חסרים
שרה(קואליציה(מנדטים))

מוחמדף הסכם_עודפים(מפלגה1, מפלגה2)
שרה(מפלגה1)
שרה(מפלגה2)
החזר מפלגה1 + " וה" + מפלגה2
סיום

~ קריאה להסכם עודפים
מתנה מפלגות = הסכם_עודפים("ליכוד", "הציונות הדתית")
שרה(מפלגות)
```
## **משתנים**
:על מנת להגדיר משתנה בשפה יש לכתוב את המילה השמורה `מתנה` ולאחריה שם המשתנה
```
מתנה א = 0
```
### :משתנים יכולים להיות מארבעה סוגים

(int\double) שוחד
```
מתנה א = 0.5
```
(string) מחרוזת
```
"מתנה א = "רק לא ביבי
```
(list) רשימה
```
מתנה א = [61, "עוגת גבינה", "ליכוד"]
```
(function) פעולה
```
מתנה א = מוחמדף קואליציה(מספר) -> 61 - מספר  
```
## **(if) תנאים** 
:כדי לכתוב תנאי בשפת ביבי יש להתחיל מהמילה השמורה `אם` כשאחריה ביטוי בוליאני
```
אם ליכוד == 1 אז
שרה("רק ביבי")
שרה(61)
סיום
```
הערה: ליכוד הוא משתנה שמור לערך `1` ומרצ לערך `0`


בנוסף, ניתן להשתמש במילה השמורה `אחרם` המייצגת את הלחמת המילים `אחרת+אם` כדי לבדוק תנאי כאשר התנאי הראשון לא תקף

```
אם ליכוד == 0 אז
שרה("רק ביבי")
אחרם מרצ == 0 אז
שרה("שמאל")
סיום
```
וכמובן המילה השמורה `אחרת` כאשר התנאי לא מתקיים
```
אם ליכוד == 0 אז
שרה("רק ביבי")
אחרת
שרה("שמאל")
שרה("רק לא ביבי")
סיום
```
וכמובן שאפשר לשלב את שלושתם
```
אם ליכוד == 0 אז
שרה("רק ביבי")
אחרם מרצ == 1 אז
שרה("רק לא ביבי")
אחרת
שרה("אני מבולבל")
```
כאשר יש רק בייטוי אחד אחרי תנאי או המילה השמורה `אחרת` אין צורך לכתוב `סיום` בסופו 
```
אם ליכוד == 1 אז
שרה("רק ביבי")
```
## **(for) לולאות בשביל**
הגדרת לולאה מורכבת מהמילה `בשביל` כשלאחריה הצהרת משתנה עם ערך התחלתי כשלאחר מכן המילה השמורה `עד` וערך יעד כשלבסוף המילה `אז` לאחר הבייטוים בתוך הלולאה
היא נסגרת במילה השמורה `סיום` 
```
בשביל א = 0 עד 10 אז
שרה(א)
סיום
```
:"ניתן לשנות את השיינוי למשתנה בכל איטרציה של הלולאה עם המילה השמורה "צעד
```
בשביל א = 0 עד 10 צעד 2 אז
שרה(א)
סיום
```

## **פונקציות (מוחמדף)**
כדי להגדיר פונקציה בשפת ביבי, יש להשתמש במילה השמורה `מוחמדף`
לאחר מכן, יש לתת שם לפונקציה. שם הפונקציה לא יכול להכיל סימנים מיוחדים (מלבד _ ), או להתחיל במספר.
לאחר שם הפונקציה יש לפתוח סוגריים ולכתוב את שמות המשתנים שהפונקציה מקבלת (אם ישנם כאלו)
בסוף הפונקציה יש  לכתוב את המילה `סיום` על מנת לסגור את הבלוק שלה
```
מוחמדף הסכם_עודפים(מפלגה1, מפלגה2)
שרה(מפלגה1)
שרה(מפלגה2)
החזר מפלגה1 + מפלגה2
סיום
```
במקרה של ביטוי אחד יש לכתוב את הפונקציה ללא המילה שמורה `סיום` בצורה הזאת
```
מוחמדף קואליציה(מספר) -> 61 - מספר
```
## **פעולות מובנות**
### כלליות 

`שרה(קלט)` הפעולה מדפיסה את הקלט למסך
```
שרה(קלט)
```
`תקשורת()` הפעולה מקבלת קלט מהמשתנה כמחרוזת
```
()מתנה א = תקשורת
```
`העלם_ראיות()` מוחקת את כל הנכתב על המסך
```
()העלם_ראיות
```
### בדיקת טיפוס
`האם_שוחד(קלט)` הפעולה מחזירה 1 אם הקלט הוא שוחד אחרת 0
```
(א)האם_שוחד
```
`האם_מחרוזת(קלט)` הפעולה מחזירה 1 אם הקלט הוא מחרוזת אחרת 0
```
(א)האם_מחרוזת
```

`האם_רשימה(קלט)` הפעולה מחזירה 1 אם הקלט הוא רשימה אחרת 0
```
(א)האם_רשימה
```

`האם_פונקציה(קלט)` הפעולה מחזירה 1 אם הקלט הוא פונקציה אחרת 0
```
(א)האם_פונקציה
```

### פעולות על רשימה
`הוסף(רשימה ,קלט)` הפעולה מוסיפה את הקלט לרשימה
```
מתנה א = [1,2,3]
הוסף(א, 4)
```
`מחק(רשימה ,מיקום)` הפעולה מוחקת את האיבר במיקום מהרשימה
```
מתנה א = [1,2,3]
מחק(א, 1)
```
`שלוף(רשימה)` הפעולה מחזירה את האיבר האחרון ברשימה
```
מתנה א = [1,2,3]
מתנה ב = שלוף(א)
```
 כדי לקבל איבר במיקום מסויים ברשימה יש לכתוב לאחר הרשימה את הסימן `$`  ולאחריו המיקום
כי רק עם כסף דברים עובדים במדינה הזאת
```
מתנה א = [1,2,3]
שרה(א $ 2)
```

`הרחב(רשימה1, הרשימה2)` הפעולה מחברת את שתי הרשימות
```
מתנה ג = הרחב([1,2,3], [4,5,6])
```
`+` בנוסף לפעולה הנ"ל אפשר לחבר רשימות בעזרת הסימן

```
מתנה ג = [1,2,3] + [4,5,6]
```
### פעולות שונות

`מחרוזת_לרשימה(מחרוזת)` הפעולה מחזירה מחרוזת בתור רשימת התווים בה
```
מחרוזת_לרשימה("רק ביבי")
```
`מחרוזת_לשוחד(מחרוזת)` הפעולה מחזירה מספר אם אפשרי מהמחרוזת
```
מחרוזת_לשוחד("61")
```
`האם_שמלאני(מחרוזת)` הפעולה מחזירה אם המחרוזת היא שמלאנית 
```
האם_שמלאני("מרצ - השמאל של ישראל")
```
`אורך(קלט)` הפעולה מחזירה את אורך הרשימה או המחרוזת 
```
אורך([1,2,3,4,5])
```
`בחירות(שם_קובץ)` הפעולה מריצה את הקובץ בשם הקלט 
```
("דוגמה.bb")בחירות
```



## ❗️**שגיאות**❗️

:להלן חלק מן השגיאות שיכולות לקרות בעת כתיבת קוד ביביתון
### **שגיאת מנתח - תו לא חוקי**
כאשר בניתוח הקוד לפני ההרצה מתגלה תו לא חוקי
```
אזרחים יקרים, התו הזה שמאלני
זה בקובץ: אה זה לא קובץ בשורה: 1
'&'
```

### **שגיאת זמן ריצה - תו לא חוקי**
כאשר בזמן הריצה מתגלה בקובץ ההרצה תו לא חוקי
```
:קראת שגיאה בזמן הריצה לממשלה
!א'? מה? מה פתאום'
```
### **שגיאת מנתח - אי סגירת ביטוי**
כאשר תנאי, לולאה או פונקציה לא נסגרו
```
לפיד כדאי שתחזור לבית הספר, כי אני לא מבין את הניסוח הזה
דוגמה בשורה: 6.bb :זה בקובץ
!התיק לא סגור
```
<div align="center">

# About
השפה **ביביתון** נכתבה על ידי

 **עידן אביעד ועילי רז**  

בשנת **2021**
</div>
</div>
