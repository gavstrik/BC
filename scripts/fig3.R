
# usefull function
clean_up <- function(...){
  for(i in dev.list()) dev.off(which=i)
  keep = as.list(match.call())
  rm(list=setdiff(ls(envir = .GlobalEnv), keep), envir = .GlobalEnv)
  # assign("savePDF", FALSE, envir = .GlobalEnv)
  assign("icloud", "~/Library/Mobile Documents/com~apple~CloudDocs/", envir = .GlobalEnv)
  cat("\014")  # Clear console
}

amt <- read.csv("~/Papers/Game of Regret/GoR_github/BC/data/amt.csv")
nagel.in <- read.csv("~/Papers/Game of Regret/GoR_github/BC/data/Nagel95.csv")

tmp1 = nagel.in[,1:2]
tmp1$round = 1
tmp1$avg = nagel.in$round.1

tmp2 = nagel.in[,1:2]
tmp2$round = 2
tmp2$avg = nagel.in$round.2

tmp3 = nagel.in[,1:2]
tmp3$round = 3
tmp3$avg = nagel.in$round.3

tmp4 = nagel.in[,1:2]
tmp4$round = 4
tmp4$avg = nagel.in$round.4

nagel = rbind(tmp1,tmp2,tmp3,tmp4)

# make an extra column specifying the group size
nagel$size = NA
for(i in 4:7){
  for(j in 1:4){
    nagel[nagel$session==i & nagel$round==j,]$size = max(nagel[nagel$session==i & nagel$round==j,]$id)
  }
}


# amt$size = as.factor(amt$size)
# amt$size = relevel(amt$size,ref = 2)

str(amt)


boxcox <- function(y, lam, eta=0){
  if(lam!=0){
    out = ((y+eta)^lam-1)/lam
  } else{
    out = log(y+eta)
  }
  return(out)
}

M0 = glm(avg ~ (round+round2)*as.factor(size)-1, data=amt)
# M1 = glm(boxcox(avg,0) ~ (round+round2)*as.factor(size)-1, data=nagel)
M1 = glm(log(avg) ~ as.factor(round)-1, data=nagel)

res = resid(M0)
res = (res-mean(res))/sd(res)
qqnorm(res); abline(0,1, col='red')

res = resid(M1)
res = (res-mean(res))/sd(res)
qqnorm(res); abline(0,1, col='red')

summary(M0)
summary(M1)

tmp1 = expand.grid(size=as.factor(c(2,4,8)),round=1:8)
tmp1$round2 = tmp1$round^2
pred = predict(M0,newdata = tmp1, se.fit = TRUE)


tmp = aggregate(avg ~ size+round, mean, data=amt)
tmp$fit = pred$fit
tmp$fit.lo = pred$fit-1.96*pred$se.fit
tmp$fit.hi = pred$fit+1.96*pred$se.fit

plot(0,0, type='n', xlim=c(1,8), ylim=c(0,60), bty='n')
size=2
plot1 <- function(size, col){

  
  # tmp3 = amt[amt$size==size,c(3,4,5,14)]
  # for(i in 1:size){
  #   for(j in unique(tmp3[tmp3$id_in_group==i,]$group)){
  #     tmp4 = tmp3[tmp3$id_in_group==i & tmp3$group==j,]
  #     lines(tmp4$round, tmp4$avg, col=add.alpha(col,.05), lty=1, lwd=1)
  #   }
  # }
  
  tmp2 = tmp[tmp$size==size,]
  polygon(c(1:8,8:1), c(tmp2$fit.lo, rev(tmp2$fit.hi)), border=NA, col=add.alpha(col,.25))
  lines(tmp2$round, tmp2$fit, col=add.alpha(col,.85), lwd=2)
  lines(tmp2$round, tmp2$avg, col=add.alpha(col,.95), lwd=2, 'p', pch=4)
}

plot1(2, 'red')
plot1(4, 'orange')
plot1(8, 'dodgerblue')


chess=c(32.15, 25.7)
w03 = c(24.6, 16.4, 6.7, 6.2, 12.1, 5.4, 9.6, 11.2, 8.4, 6.5)
kd08.14 = c(35.3,21.5, 17.1, 14.0, 13.4)
kd08.50 = c(35.7, 25.1, 15.9, 12.2, 12.9)
kd08.188 = c(30.0, 21.9, 15.7, 13.6, 10.8)
n95 = c(36.732835820895524, 24.168656716417914, 16.135820895522386,9.52000014925373)

# lines(1:2, chess,    type='p', lty=5, pch=16, lwd=2)
# lines(1:10, w03,     type='p', lty=2, pch=2, lwd=1)
# lines(1:5, kd08.14,  type='p', lty=3, pch=3, lwd=2)
# lines(1:5+.05, kd08.50,  type='p', lty=4, pch=4, lwd=2)
# lines(1:5-.05, kd08.188, type='p', lty=2, pch=1, lwd=1)
# lines(1:4-.05, n95,      type='p', lty=1, pch=3, lwd=1)
lines(1:2, chess,    type='b', lty=3, pch=1, lwd=1)
lines(1:10, w03,     type='b', lty=3, pch=2, lwd=1)
lines(1:5, kd08.14,  type='b', lty=3, pch=3, lwd=1)
lines(1:5+.05, kd08.50,  type='b', lty=3, pch=6, lwd=1)
lines(1:5-.05, kd08.188, type='b', lty=3, pch=5, lwd=1)
lines(1:4-.05, n95,      type='b', lty=3, pch=0, lwd=1)


legend("topright", c('AMT (n=2, N=100)', 'AMT (n=4, N=92)', 'AMT (n=8, N=104)', 
                      'BF10 (chess players, n=13-897, N=2481)',
                     'W03 (students, n=8-10, N=26)',
                     'KD08 (students, N=14)', 
                     'KD08 (students, N=50)',
                     'KD08 (students, N=188)',
                     'N95 (students, n=15, N=64)'), bty='n', pch=c(4,4,4,16,2,3,4,1,3), col=c("red","orange","dodgerblue","black","black","black","black","black","black"))


# tmp = aggregate(avg ~ round, mean, data=nagel)
# pred = predict(M1,newdata = data.frame(round=1:4), se.fit = TRUE)
# tmp$fit = exp(pred$fit)
# tmp$fit.lo = exp(pred$fit-1.96*pred$se.fit)
# tmp$fit.hi = exp(pred$fit+1.96*pred$se.fit)
# 
# points(tmp$avg, pch=16)
# points(tmp$fit, pch=4)
# segments(1:4, tmp$fit.lo, 1:4, tmp$fit.hi)


# hist(log(nagel$avg), breaks=100, xlim=c(0,5), prob=TRUE)
# curve(dnorm(x,mean(log(nagel$avg)), sd= sd(log(nagel$avg))), add=TRUE, col='red', lwd=2)
# 
# hist(nagel$avg, breaks=100, xlim=c(0,100), prob=TRUE)
# curve(dlnorm(x,mean(log(nagel$avg)), sd= sd(log(nagel$avg))), add=TRUE, col='red', lwd=2)
# curve(dpois(x, median(nagel$avg)), add=TRUE, col='red', lwd=2)
# curve(dgamma(x, 15, 5), add=TRUE, col='red', lwd=2)

# tmp2 = tmp[tmp$size==size,]
# polygon(c(1:8,8:1), c(tmp2$fit.lo, rev(tmp2$fit.hi)), border=NA, col=add.alpha(col,.25))
# lines(tmp2$round, tmp2$fit, col=add.alpha(col,.85), lwd=2)
# lines(tmp2$round, tmp2$avg, col=add.alpha(col,.95), lwd=2, 'p', pch=16)




# 
# # data from Bühren & Frank 2010:
# [32.15, 25.7], legend: 'BF10 (chess players, n=13-897, N=2481)'
# 
# # data from Weber (2003):
# [24.6, 16.4, 6.7, 6.2, 12.1, 5.4, 9.6, 11.2, 8.4, 6.5], legend: 'W03
# (students, n=8-10, N=26)'
# 
# # data from Kamm & Dahinden, 2008, taken from Diekmann 2009, [35.3,
# 21.5, 17.1, 14.0, 13.4],legend: 'KD08 (students, N=14)'
# [35.7, 25.1, 15.9, 12.2, 12.9],legend: 'KD08 (students, N=50)'
# [30.0, 21.9, 15.7, 13.6, 10.8],legend: 'KD08 (students, N=188)'
# 
# # data from Nagel 1995
# [36.732835820895524, 24.168656716417914, 16.135820895522386,
#   9.52000014925373], legend: 'N95 (students, n=15, N=64)'




M0 = glm(avg ~ (round+round2)*as.factor(size)-1, data=amt[amt$round<5,])
res = resid(M0)
res = (res-mean(res))/sd(res)
# qqnorm(res); abline(0,1, col='red')

summary(M0)


tmp = amt[amt$round<5,]
tmp$size2 = 1*(tmp$size==2)

M1 = glm(avg ~ round*as.factor(size)-1, data=tmp)
# res = resid(M1)
# res = (res-mean(res))/sd(res)
# qqnorm(res); abline(0,1, col='red')

anova(M0,M1,test='LRT')
summary(M1)

# M2 = glm(avg ~ round*size2-1, data=tmp)
# summary(M2)
# 
# anova(M1,M2,test='LRT')

n.tmp = coef(lm(avg ~ round, data=aggregate(avg ~ round, mean, data=nagel)))




b1 = c(1,0,0,0,0,0)
b2 = c(1,0,0,0,1,0)
b3 = c(1,0,0,0,0,1)

1-pt((t(b1)%*%coef(M1)-n.tmp[2])/sqrt(t(b1)%*%vcov(M1)%*%b1),1)
1-pt((t(b2)%*%coef(M1)-n.tmp[2])/sqrt(t(b2)%*%vcov(M1)%*%b2),1)
1-pt((t(b3)%*%coef(M1)-n.tmp[2])/sqrt(t(b3)%*%vcov(M1)%*%b3),1)

n.tmp


grps =rbind(c(t(b1)%*%coef(M1)-1.96*sqrt(t(b1)%*%vcov(M1)%*%b1),t(b1)%*%coef(M1)+1.96*sqrt(t(b1)%*%vcov(M1)%*%b1)),
            c(t(b2)%*%coef(M1)-1.96*sqrt(t(b2)%*%vcov(M1)%*%b2),t(b2)%*%coef(M1)+1.96*sqrt(t(b2)%*%vcov(M1)%*%b2)),
            c(t(b3)%*%coef(M1)-1.96*sqrt(t(b3)%*%vcov(M1)%*%b3),t(b3)%*%coef(M1)+1.96*sqrt(t(b3)%*%vcov(M1)%*%b3)))

rownames(grps) <- c(2,4,8)
colnames(grps) <- c("lo","hi")
grps


c(coef(lm(chess ~ c(1,2)))[2],
  coef(lm(w03[1:4] ~ c(1:4)))[2],
  coef(lm(kd08.14[1:4] ~ c(1:4)))[2],
  coef(lm(kd08.50[1:4] ~ c(1:4)))[2],
  coef(lm(kd08.188[1:4] ~ c(1:4)))[2],
  coef(lm(avg ~ round, data=aggregate(avg ~ round, mean, data=nagel)))[2])


summary(M1)

coef(M1)

sqrt(diag(vcov(M1)))

coef(M1)[1]
sum(coef(M1)[c(1,5)])
sum(coef(M1)[c(1,6)])





# n.tmp = 
# /n.tmp$avg[4]/4
# diff(n.tmp$avg[c(4,1)])/n.tmp$avg[1]
# diff(n.tmp$avg[c(4,1)])/(4-1)



