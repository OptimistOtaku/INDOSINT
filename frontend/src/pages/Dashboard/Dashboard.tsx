import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  IconButton,
  Paper,
  LinearProgress,
  Divider,
} from '@mui/material';
import {
  Search,
  Analytics,
  Face,
  Dna,
  Timeline,
  TrendingUp,
  Security,
  Notifications,
  MoreVert,
  Visibility,
  Warning,
  CheckCircle,
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { motion } from 'framer-motion';

import { useAuth } from '../../contexts/AuthContext';
import { dashboardAPI } from '../../services/api';
import { DashboardStats, RecentActivity, QuickAction } from '../../types/dashboard';
import { SearchCard } from '../../components/Search/SearchCard';
import { ActivityChart } from '../../components/Charts/ActivityChart';
import { RiskIndicator } from '../../components/Indicators/RiskIndicator';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [selectedTimeframe, setSelectedTimeframe] = useState('7d');

  // Fetch dashboard data
  const { data: stats, isLoading: statsLoading } = useQuery<DashboardStats>(
    ['dashboard-stats', selectedTimeframe],
    () => dashboardAPI.getStats(selectedTimeframe),
    { refetchInterval: 300000 } // Refetch every 5 minutes
  );

  const { data: recentActivity, isLoading: activityLoading } = useQuery<RecentActivity[]>(
    ['recent-activity'],
    () => dashboardAPI.getRecentActivity(),
    { refetchInterval: 60000 } // Refetch every minute
  );

  const { data: quickActions } = useQuery<QuickAction[]>(
    ['quick-actions'],
    () => dashboardAPI.getQuickActions()
  );

  const StatCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ReactNode;
    color: string;
    trend?: number;
    subtitle?: string;
  }> = ({ title, value, icon, color, trend, subtitle }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${color}20, ${color}10)` }}>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Box>
              <Typography variant="h4" component="div" fontWeight="bold">
                {value}
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {title}
              </Typography>
              {subtitle && (
                <Typography variant="caption" color="text.secondary">
                  {subtitle}
                </Typography>
              )}
              {trend !== undefined && (
                <Box display="flex" alignItems="center" mt={1}>
                  <Chip
                    icon={trend > 0 ? <TrendingUp /> : <TrendingUp sx={{ transform: 'rotate(180deg)' }} />}
                    label={`${Math.abs(trend)}%`}
                    size="small"
                    color={trend > 0 ? 'success' : 'error'}
                    variant="outlined"
                  />
                </Box>
              )}
            </Box>
            <Avatar sx={{ bgcolor: color, width: 56, height: 56 }}>
              {icon}
            </Avatar>
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );

  const ActivityItem: React.FC<{ activity: RecentActivity }> = ({ activity }) => (
    <ListItem>
      <ListItemAvatar>
        <Avatar sx={{ bgcolor: activity.type === 'search' ? 'primary.main' : 'secondary.main' }}>
          {activity.type === 'search' ? <Search /> : <Analytics />}
        </Avatar>
      </ListItemAvatar>
      <ListItemText
        primary={activity.title}
        secondary={
          <Box>
            <Typography variant="body2" color="text.secondary">
              {activity.description}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {new Date(activity.timestamp).toLocaleString()}
            </Typography>
          </Box>
        }
      />
      <IconButton size="small">
        <MoreVert />
      </IconButton>
    </ListItem>
  );

  const QuickActionCard: React.FC<{ action: QuickAction }> = ({ action }) => (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <Card
        sx={{
          cursor: 'pointer',
          height: '100%',
          '&:hover': {
            boxShadow: 4,
          },
        }}
      >
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Avatar sx={{ bgcolor: action.color, mr: 2 }}>
              {action.icon}
            </Avatar>
            <Typography variant="h6" component="div">
              {action.title}
            </Typography>
          </Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            {action.description}
          </Typography>
          <Button
            variant="outlined"
            size="small"
            startIcon={action.buttonIcon}
            sx={{ mt: 1 }}
          >
            {action.buttonText}
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  );

  return (
    <Box sx={{ p: 3 }}>
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box mb={3}>
          <Typography variant="h4" component="h1" gutterBottom>
            Welcome back, {user?.full_name || user?.username}!
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Here's what's happening with your OSINT investigations today.
          </Typography>
        </Box>
      </motion.div>

      {/* Stats Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Searches"
            value={stats?.totalSearches || 0}
            icon={<Search />}
            color="#2196f3"
            trend={12}
            subtitle="Last 7 days"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Active Investigations"
            value={stats?.activeInvestigations || 0}
            icon={<Analytics />}
            color="#f50057"
            trend={-5}
            subtitle="Currently running"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Face Matches"
            value={stats?.faceMatches || 0}
            icon={<Face />}
            color="#4caf50"
            trend={8}
            subtitle="High confidence"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Risk Alerts"
            value={stats?.riskAlerts || 0}
            icon={<Security />}
            color="#ff9800"
            trend={15}
            subtitle="Requires attention"
          />
        </Grid>
      </Grid>

      {/* Main Content */}
      <Grid container spacing={3}>
        {/* Search Interface */}
        <Grid item xs={12} lg={8}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quick Search
                </Typography>
                <SearchCard />
              </CardContent>
            </Card>
          </motion.div>

          {/* Activity Chart */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Search Activity
                </Typography>
                <ActivityChart timeframe={selectedTimeframe} />
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} lg={4}>
          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quick Actions
                </Typography>
                <Grid container spacing={2}>
                  {quickActions?.map((action, index) => (
                    <Grid item xs={12} key={index}>
                      <QuickActionCard action={action} />
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recent Activity
                </Typography>
                {activityLoading ? (
                  <LinearProgress />
                ) : (
                  <List>
                    {recentActivity?.map((activity, index) => (
                      <React.Fragment key={activity.id}>
                        <ActivityItem activity={activity} />
                        {index < recentActivity.length - 1 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 