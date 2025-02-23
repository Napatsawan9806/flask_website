Enrollment system Website

เป็นเว็บไซต์สำหรับการลงทะเบียนเรียนในแต่บะรายวิชา ซึ่งมีการ register และ log in เพื่อเข้าสู่ระบบ ต้องเข้าสู้ระบบเท่านั้นจึงจะสามารถเข้าสู๋หน้า Dashboard เพื่อทำการลงทะเบียนได้ ซึ่งในหน้า Dashboard จะมีให้เข้าไปดูตารางที่ได้มีการละเบียนไว้ และการถอนรายวิชาออก 
ส่วนของ admin จะมี admin panel เพิ่มขึ้นมาซึ่งสามารถเพิ่มรายวิชาเรียน แก้ไขรายละเอียดของวิชาเรียน และการลบรายวิชาเรียน 

วิธีการรันเว็บนี้ 
1. pull git นี้ไปทั้งหมด
2. activate virtual enviroment
3. ใช้ poetry run python .\project\app.py เพื่อรัน

หากต้องการเข้าในฐานะนักศึกษา สามารถ register และ log in เพื่อใช้งานได้ปกติ แต่หากต้องการเข้าในฐานะ admin ให้ log in โดยใช้ 
username : admin, password : admin123

อธิบายแต่ละไฟล์ :
1. instance
     ใช้ในการดู database
2. CSS\base.css
     ใช้ในการตกแต่งหน้าเว็บ ซึ่งมีไฟล์เดียวเพราะไฟล์ .html ทุกไฟล์ใช้ template จาก base.html จึงเพิ่มคลาสใน base.css และเรียกใช้ในแต่ละไฟล์ของ .html แทน
3. templates
     โฟลเดอร์ที่ใช้เก็บไฟล์ html
4. forms.py
     ใช้ในการสร้างฟอร์มในการ register และ log in
5. models.py
     model ของ database ว่าจะมีการเก็บข้อมูลในตารางไหนบ้าง
6. decorators.py
     ไฟล์เพื่อสร้างฟังก์ชัน admin_required เพื่อใช้ในการบังคับว่าการจะเข้า admin panel ได้ จะต้อง log in ด้วย role ของ aadmin เท่านั้น
7. app.py
     ไฟล์หลักเพื่อใช้ในการรันเว็บ และระบุ path ของเว็บ เช่น /dashboard/schedule ซึ่งในไฟล์นี้จะมีการ import จากไฟล์ forms, models, decorators เพื่อนำ class หรือ function แต่ละตัวมาใช้

  db.init_app(app)
  bcrypt.init_app(app)          ตรงส่วนนี้จะเป็นการเชื่อมกับ database
  migrate = Migrate(app, db)
  
  เริ่มแรกจะมีการใช้ @login_manager.user_loader เพื่อโหลดข้อมูลของผู้ใช้ที่ยัง log in อยู่มา ทำให้ไม่ต้อง log in ใหม่ทุกครั้ง

  ส่วนต่อไปจะเป็น app.route(....) ซึ่งเป็นการระบุเส้นทางตามที่ได้กล่าวไว้ และการจัดการต่างๆภายใน path นั้น
  ซึ่งมีหน้า home, login, register, dashboard, enroll, schedule, withdraw และสำหรับ admin จะมีหน้า manage, edit course เพิ่มมาด้วย

  และ app.run(debug = True) เพื่อรันไฟล์นี้
