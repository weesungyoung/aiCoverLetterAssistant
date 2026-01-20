const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const { User } = require('../models');

router.post('/join', async (req, res) => {
  try {
    const { email, password, nickName } = req.body;

    if (!email || !password || !nickName) {
      return res.status(400).json({ message: '모든 필드를 입력해주세요.' });
    }

    const existingUser = await User.findOne({ where: { userEmail: email } });
    if (existingUser) {
      return res.status(400).json({ message: '이미 사용 중인 이메일입니다.' });
    }

    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    const newUser = await User.create({
      userEmail: email,
      userPassword: hashedPassword,
      nickName: nickName
    });

    res.status(201).json({ 
      message: '회원가입이 완료되었습니다!',
      user: { email: newUser.userEmail, nickName: newUser.nickName } 
    });

  } catch (error) {
    console.error(error);
    res.status(500).json({ message: '서버 내부 오류가 발생했습니다.' });
  }
});

module.exports = router;